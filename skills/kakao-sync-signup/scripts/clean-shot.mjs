// clean-shot.mjs — take a console screenshot that is safe for a blog post or a public repo.
//
// Usage inside an `ego-browser nodejs` script:
//   const { cleanShot } = await import("/abs/path/skills/kakao-sync-signup/scripts/clean-shot.mjs");
//   await cleanShot(page, "/abs/path/docs/screenshots/01-create-app.png", { focus, blur, hide, fullPage });
//
// Display-only changes (no form value changes, nothing is saved); all are undone after the shot:
//   1. Hides page headers (they show the signed-in person's name or email).
//   2. Covers with a solid box any text or input value that looks like an email (also a truncated
//      one such as "name@gmail..."), a business registration number, a phone number, or a key/secret.
//   3. Blurs everything outside the focus element (default: an open dialog), so an open dialog does
//      not show the list behind it.
// Works across open shadow roots and same-origin iframes (Kakao Business renders inside both).
// It cannot reach a cross-origin iframe, such as the Kakao consent preview: use the email-parameter
// swap in references/evidence-pack.md for that screen.
// Always run scripts/scan-shots.swift on the result, and look at each image once. The OCR scan catches
// most leaks but missed a small white-on-blue name badge in a test, so it is a second net, not proof.

export async function cleanShot(page, path, opts = {}) {
  const hideSel = opts.hide || [];
  const blurSel = opts.blur || [];
  const focusSel = opts.focus === undefined
    ? '[role=dialog], [aria-modal="true"], iframe[src*="/wizard/"]'
    : opts.focus;
  const res = await page.evaluate(([hideSel, blurSel, focusSel]) => {
    const roots = [];
    const walk = (root) => {
      roots.push(root);
      root.querySelectorAll("*").forEach((el) => { if (el.shadowRoot) walk(el.shadowRoot); });
      root.querySelectorAll("iframe").forEach((f) => { try { if (f.contentDocument) walk(f.contentDocument); } catch (_) {} });
    };
    walk(document);
    const all = (sel) => roots.flatMap((r) => { try { return [...r.querySelectorAll(sel)]; } catch (_) { return []; } });
    const up = (n) => n.parentElement || (n.getRootNode && n.getRootNode().host) || null;
    const touched = [];
    const save = (el, key, props) => { if (el.dataset[key]) return false; el.dataset[key] = JSON.stringify(Object.fromEntries(props.map((p) => [p, el.style[p]]))); touched.push(el); return true; };
    const redact = (el) => {
      if (!el || !el.style || !save(el, "cleanShotRedact", ["color", "background", "textShadow", "webkitTextFillColor"])) return;
      el.style.color = "transparent"; el.style.webkitTextFillColor = "transparent"; el.style.textShadow = "none"; el.style.background = "#9aa19c";
    };
    const hide = (el) => { if (el && el.style && save(el, "cleanShotVis", ["visibility"])) el.style.visibility = "hidden"; };
    const blurBg = (el) => { if (el && el.style && save(el, "cleanShotBlur", ["filter"])) el.style.filter = "blur(10px)"; };

    const missed = blurSel.filter((s) => all(s).length === 0);
    if (missed.length) return { error: "blur selector matched nothing: " + missed.join(", ") };

    const patterns = [
      /[A-Za-z0-9._%+*-]{2,}@[A-Za-z0-9-]+/,                      // email, also truncated "name@gmail..." and starred "abc***@example.com"
      /\b\d{3}\s?-\s?\d{2}\s?-\s?\d{5}\b/,                        // business registration number
      /\b\d{10}\b/,                                                 // business registration number typed without hyphens
      /\b\d{6}\s?-\s?[1-8]\d{6}\b/,                                // 주민등록번호 (resident registration number)
      /\b01[016-9]-?\d{3,4}-?\d{4}\b/,                            // mobile phone
      /\b[0-9a-fA-F]{24,}\b/,                                      // hex keys
      /\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{20,}\b/, // keys, client secrets
    ];
    const hit = (s) => patterns.some((p) => p.test(s || ""));

    all('header, [class*="gnb" i], [class*="Header" i]').forEach((el) => { if (!el.querySelector("main")) hide(el); });
    hideSel.forEach((s) => all(s).forEach(hide));
    blurSel.forEach((s) => all(s).forEach(redact));
    roots.forEach((r) => {
      const w = (r.ownerDocument || r).createTreeWalker(r, NodeFilter.SHOW_TEXT);
      for (let n = w.nextNode(); n; n = w.nextNode()) if (hit(n.nodeValue)) redact(n.parentElement);
    });
    all("input, textarea").forEach((el) => { if (hit(el.value)) redact(el); });

    const focus = focusSel ? all(focusSel).find((el) => el.getBoundingClientRect().width > 0) : null;
    if (focus) {
      for (let node = focus; node && node !== document.body && node !== document.documentElement; node = up(node)) {
        const parent = up(node);
        if (!parent) break;
        const kids = parent.shadowRoot && node.getRootNode() === parent.shadowRoot ? [...parent.shadowRoot.children] : [...parent.children];
        kids.forEach((sib) => { if (sib !== node && !sib.contains(focus)) blurBg(sib); });
      }
    }
    window.__cleanShotRoots = roots.length;
    return { count: touched.length, roots: roots.length, focus: !!focus };
  }, [hideSel, blurSel, focusSel]);
  if (res && res.error) throw new Error("clean-shot refused to capture: " + res.error);
  await page.waitForTimeout(150);
  const out = await page.screenshot({ path, fullPage: !!opts.fullPage });
  await page.evaluate(() => {
    const roots = [];
    const walk = (root) => {
      roots.push(root);
      root.querySelectorAll("*").forEach((el) => { if (el.shadowRoot) walk(el.shadowRoot); });
      root.querySelectorAll("iframe").forEach((f) => { try { if (f.contentDocument) walk(f.contentDocument); } catch (_) {} });
    };
    walk(document);
    for (const key of ["cleanShotRedact", "cleanShotVis", "cleanShotBlur"]) {
      const attr = "data-" + key.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());
      roots.forEach((r) => r.querySelectorAll(`[${attr}]`).forEach((el) => {
        const saved = JSON.parse(el.dataset[key]); Object.entries(saved).forEach(([p, v]) => { el.style[p] = v; }); delete el.dataset[key];
      }));
    }
  });
  return { path: out, ...res };
}
