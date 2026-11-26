// scan-shots.swift — read the text in screenshots with macOS Vision OCR and flag personal data.
//
// Usage:
//   swift scan-shots.swift <png-or-folder> [--deny "name1,name2"] [--redact]
// --redact covers each flagged OCR line with a solid box and overwrites the file (PNG). Scan again after.
// Exit code 1 if any screenshot holds an email, a business registration number,
// a phone number, a long key-like token, or any --deny word (예: the owner's name).
// Run it on every screenshot before a commit, a blog post or a public repo push.
// Why: on 2026-11-25 a blur selector missed untyped <input> fields and a screenshot
// showed the representative's name and the company address. Eyes missed it at first.

import Foundation
import Vision
import AppKit

var args = Array(CommandLine.arguments.dropFirst())
var deny: [String] = []
var redact = false
if let r = args.firstIndex(of: "--redact") { redact = true; args.remove(at: r) }
if let i = args.firstIndex(of: "--deny"), i + 1 < args.count {
    deny = args[i + 1].split(separator: ",").map { String($0).trimmingCharacters(in: .whitespaces) }.filter { !$0.isEmpty }
    args.removeSubrange(i...(i + 1))
}
guard let target = args.first else { print("usage: swift scan-shots.swift <png|folder> [--deny a,b]"); exit(2) }

var files: [URL] = []
var isDir: ObjCBool = false
if FileManager.default.fileExists(atPath: target, isDirectory: &isDir), isDir.boolValue {
    let items = (try? FileManager.default.contentsOfDirectory(atPath: target)) ?? []
    files = items.filter { $0.lowercased().hasSuffix(".png") || $0.lowercased().hasSuffix(".jpg") }.sorted()
        .map { URL(fileURLWithPath: target).appendingPathComponent($0) }
} else { files = [URL(fileURLWithPath: target)] }

let patterns: [(String, String)] = [
    ("email", "[A-Za-z0-9._%+*-]{2,}@[A-Za-z0-9-]+"),
    ("business-number", "\\b\\d{3}\\s?-\\s?\\d{2}\\s?-\\s?\\d{5}\\b"),
    ("business-number", "\\b\\d{10}\\b"),
    ("resident-number", "\\b\\d{6}\\s?-\\s?[1-8]\\d{6}\\b"),
    ("phone", "\\b01[016-9]\\s?-?\\s?\\d{3,4}\\s?-?\\s?\\d{4}\\b"),
    ("key-like", "\\b(?=[A-Za-z0-9_-]*\\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{20,}\\b"),
]
// Placeholders written by the masking steps. Prefix match: the email pattern can stop before the TLD.
let allow = ["user@example.com"]

var bad = 0
for url in files {
    guard let img = NSImage(contentsOf: url), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("SKIP  \(url.lastPathComponent) (cannot read)"); continue
    }
    // Vision downsamples a whole large capture and then misses console-size text (it read the
    // email in a 600x300 crop but not in the 3000x1377 capture). Read overlapping tiles instead.
    var lines: [String] = []
    var boxes: [(String, CGRect)] = []   // text with its box in top-left pixel coordinates
    let tile = 700, step = 560
    var y = 0
    while y < cg.height {
        var x = 0
        while x < cg.width {
            let rect = CGRect(x: x, y: y, width: min(tile, cg.width - x), height: min(tile, cg.height - y))
            if let part = cg.cropping(to: rect) {
                let req = VNRecognizeTextRequest()
                req.recognitionLevel = .accurate
                req.recognitionLanguages = ["ko-KR", "en-US"]
                req.usesLanguageCorrection = false
                try? VNImageRequestHandler(cgImage: part, options: [:]).perform([req])
                for o in (req.results ?? []) {
                    guard let t = o.topCandidates(1).first?.string else { continue }
                    lines.append(t)
                    let b = o.boundingBox
                    let px = CGRect(x: CGFloat(x) + b.minX * rect.width, y: CGFloat(y) + (1 - b.maxY) * rect.height,
                                    width: b.width * rect.width, height: b.height * rect.height)
                    boxes.append((t, px))
                }
            }
            if x + tile >= cg.width { break }
            x += step
        }
        if y + tile >= cg.height { break }
        y += step
    }
    var hits: [String] = []
    for line in lines {
        for (name, p) in patterns {
            if let r = line.range(of: p, options: .regularExpression) {
                let s = String(line[r]); if !allow.contains(where: { s.hasPrefix($0) || $0.hasPrefix(s) }) { hits.append("\(name): \(s.prefix(6))…") }
            }
        }
        for w in deny where line.contains(w) { hits.append("deny-word: \(w.prefix(1))…") }
    }
    if redact && !hits.isEmpty {
        // Cover every OCR line that triggered a hit with a solid box and overwrite the file.
        let bad = boxes.filter { (t, _) in
            patterns.contains { (_, p) in t.range(of: p, options: .regularExpression).map { r in !allow.contains(where: { String(t[r]).hasPrefix($0) || $0.hasPrefix(String(t[r])) }) } ?? false }
            || deny.contains { t.contains($0) }
        }
        let cs = CGColorSpaceCreateDeviceRGB()
        if let ctx = CGContext(data: nil, width: cg.width, height: cg.height, bitsPerComponent: 8, bytesPerRow: 0, space: cs,
                               bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) {
            ctx.draw(cg, in: CGRect(x: 0, y: 0, width: cg.width, height: cg.height))
            ctx.setFillColor(CGColor(red: 0.60, green: 0.63, blue: 0.61, alpha: 1))
            for (_, r) in bad {
                let pad: CGFloat = 4
                ctx.fill(CGRect(x: r.minX - pad, y: CGFloat(cg.height) - r.maxY - pad, width: r.width + 2 * pad, height: r.height + 2 * pad))
            }
            if let out = ctx.makeImage() {
                let rep = NSBitmapImageRep(cgImage: out)
                if let data = rep.representation(using: .png, properties: [:]) { try? data.write(to: url) }
                print("FIXED \(url.lastPathComponent): covered \(bad.count) line(s); run the scan again")
            }
        }
    }
    if hits.isEmpty { print("OK    \(url.lastPathComponent) (\(lines.count) lines)") }
    else { bad += 1; print("LEAK  \(url.lastPathComponent): \(Set(hits).sorted().joined(separator: ", "))") }
}
exit(bad > 0 ? 1 : 0)
