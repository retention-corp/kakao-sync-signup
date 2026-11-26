#!/usr/bin/env python3
"""Pre-submit check for a Kakao Sync setup.

Usage:
  python3 -I precheck.py <intake.json> [--privacy-text FILE] [--term-text TAG=FILE ...] [--offline]

Reads the intake JSON described in references/intake-template.md, fetches every public URL,
and checks the rules in references/review-checklist.md and references/ad-consent-rules.md
that a script can see. Prints one line per check: PASS, WARN or FAIL. Exit code 1 if any
FAIL. Standard library only.

Use --privacy-text / --term-text when a page renders with JavaScript: extract its visible
text in ego-browser, save it to a file, and pass the file here.
"""

import argparse
import html
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) kakao-sync-precheck"
TIMEOUT = 15

# python.org builds on macOS ship without a CA bundle. Add the system bundle; keep verification on.
SSL_CTX = ssl.create_default_context()
if os.path.exists("/etc/ssl/cert.pem"):
    SSL_CTX.load_verify_locations("/etc/ssl/cert.pem")

# Keywords that show an item is named in the privacy policy.
SCOPE_KEYWORDS = {
    "profile_nickname": ["닉네임"],
    "profile_image": ["프로필 사진", "프로필사진", "프로필 이미지"],
    "account_email": ["이메일", "e-mail", "email", "전자우편"],
    "name": ["이름", "성명"],
    "gender": ["성별"],
    "age_range": ["연령대", "연령"],
    "birthday": ["생일", "생년월일"],
    "birthyear": ["출생 연도", "출생연도", "출생년도", "생년"],
    "phone_number": ["전화번호", "휴대전화", "휴대폰", "연락처"],
    "account_ci": ["연계정보", "CI"],
    "shipping_address": ["배송지", "주소"],
    "plusfriends": ["카카오톡 채널", "채널 추가", "채널"],
}
SCOPE_LABEL = {
    "profile_nickname": "닉네임", "profile_image": "프로필 사진", "account_email": "이메일",
    "name": "이름", "gender": "성별", "age_range": "연령대", "birthday": "생일",
    "birthyear": "출생 연도", "phone_number": "전화번호", "account_ci": "CI(연계정보)",
    "shipping_address": "배송지", "plusfriends": "카카오톡 채널 추가",
}
AD_HINTS = ["광고", "마케팅", "혜택", "이벤트", "정보제공", "정보 제공", "소식", "알림"]
BANNED_AD_TITLES = ["마케팅 동의", "마케팅 활용", "마케팅 수신", "혜택 알림", "혜택알림",
                    "정보제공 동의", "정보 제공 동의", "이벤트 알림", "소식 받기"]
TAG_RE = re.compile(r"^[A-Za-z0-9_-]+$")

results = []


def out(level, check, msg):
    results.append(level)
    print(f"{level:4}  {check:28}  {msg}")


def norm(s):
    return re.sub(r"\s+", "", s or "")


def fetch(url):
    """Return (status, final_url, text) or (None, None, error message)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ko"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as r:
            raw = r.read(3_000_000)
            charset = r.headers.get_content_charset() or "utf-8"
            body = raw.decode(charset, errors="replace")
            return r.status, r.geturl(), html_to_text(body)
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # network, TLS, timeout
        return None, None, str(e)


def html_to_text(body):
    body = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", html.unescape(body)).strip()


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return re.sub(r"\s+", " ", f.read())


def check_url(check, url, offline, require_https=True):
    if not url:
        out("FAIL", check, "URL is missing")
        return None
    if require_https and not url.startswith("https://"):
        out("FAIL", check, f"not https: {url}")
    if offline:
        out("WARN", check, f"offline: not fetched {url}")
        return None
    status, final, text = fetch(url)
    if status is None:
        out("FAIL", check, f"unreachable {url}: {text}")
        return None
    if status != 200:
        out("FAIL", check, f"HTTP {status} for {url}")
        return None
    if final and final.rstrip("/") != url.rstrip("/"):
        if re.search(r"login|signin|auth", final, re.I):
            out("FAIL", check, f"redirects to a login page: {final}")
            return None
        out("WARN", check, f"redirects {url} -> {final}")
    out("PASS", check, f"HTTP 200 {url}")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("intake")
    ap.add_argument("--privacy-text")
    ap.add_argument("--term-text", action="append", default=[], help="TAG=FILE")
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()

    with open(a.intake, encoding="utf-8") as f:
        it = json.load(f)
    term_text_override = dict(x.split("=", 1) for x in a.term_text)
    scopes = it.get("scopes", [])
    terms = it.get("terms", [])
    scope_ids = {s["id"] for s in scopes if s.get("level") in ("required", "optional", "on_demand")}

    print(f"Kakao Sync precheck: {it.get('service_name')} (app {it.get('app_id')})")

    # --- Site and sign-up page -------------------------------------------------
    shared = re.search(r"\.(github\.io|workers\.dev|pages\.dev|vercel\.app|netlify\.app|web\.app|firebaseapp\.com)(/|$)|sites\.google\.com|blog\.naver\.com|tistory\.com|notion\.site",
                       it.get("site_url") or "")
    if shared:
        out("WARN", "site.own_domain", f"site is on a shared host ({shared.group(0)}); Kakao refuses blogs, shared domains and static-only hosting for business-info review (DevTalk 142570/4, 145500/4)")
    site = check_url("site.reachable", it.get("site_url"), a.offline)
    bn = re.sub(r"\D", "", it.get("business_number") or "")
    if site is not None and bn:
        if bn in re.sub(r"\D", "", site):
            out("PASS", "site.business_number", "business number found in site text")
        else:
            out("WARN", "site.business_number", "business number not in site text; Kakao matches the footer number to the app (DevTalk 149033/3)")
    signup = check_url("signup.reachable", it.get("signup_url"), a.offline)
    if signup is not None:
        name = it.get("service_name", "")
        if name and norm(name).lower() not in norm(signup).lower():
            out("WARN", "signup.service_name", f"'{name}' not found in page text (may be in an image or rendered by JS)")
        if "카카오" not in signup and "kakao" not in signup.lower():
            out("WARN", "signup.kakao_button", "no '카카오'/'kakao' text on sign-up page; check the login button in ego-browser")
        company = it.get("company_name")
        if company and norm(company) not in norm(signup):
            out("WARN", "site.company_name", f"'{company}' not in sign-up page text; reviewers want the company name on the site")

    # --- Redirect URIs ---------------------------------------------------------
    for uri in it.get("redirect_uris", []):
        if uri.startswith("http://") and not re.match(r"http://(localhost|127\.0\.0\.1)", uri):
            out("WARN", "redirect.https", f"http redirect URI: {uri}")
        if "?" in uri:
            out("WARN", "redirect.query", f"query string in redirect URI ({uri}); doc says the path cannot carry arbitrary parameters. It must match the request byte for byte")
    if not it.get("redirect_uris"):
        out("FAIL", "redirect.present", "no redirect URI in intake")

    # --- Scopes ----------------------------------------------------------------
    for s in scopes:
        sid, level = s.get("id"), s.get("level")
        purpose = (s.get("purpose") or "").strip()
        if level in ("required", "optional") and not purpose:
            out("FAIL", f"scope.purpose.{sid}", "purpose (동의 목적) is empty")
        if re.search(r"본인\s*(인증|확인)", purpose) and sid != "account_ci":
            out("WARN", f"scope.purpose.{sid}", "purpose says 본인인증/본인확인; Kakao told an applicant that Kakao Login is not identity verification")
    if "account_ci" in scope_ids and not it.get("own_identity_verification"):
        out("FAIL", "scope.ci", "CI requested but the sign-up has no own identity verification; Kakao rejected exactly this for a live app (2026-11-24)")
    if not it.get("channel_public_id"):
        out("FAIL", "channel.linked", "no channel_public_id: 간편가입 needs a business channel linked to the app (kakaologin/prerequisite)")
    for s in scopes:
        if s.get("id") == "plusfriends" and s.get("level") == "required":
            out("FAIL", "scope.plusfriends_level", "plusfriends as 필수: channel-add is an ad consent and cannot be required (DevTalk 148458/14); use 선택")
        if s.get("id") == "phone_number" and s.get("level") == "required":
            out("WARN", "scope.phone_empty", "phone_number 필수: users without KakaoTalk still have no number; the app must handle an empty value")

    # --- Privacy policy --------------------------------------------------------
    privacy = None
    if a.privacy_text:
        privacy = read_file(a.privacy_text)
        out("PASS", "privacy.text", f"using text from {a.privacy_text}")
        if not a.offline:
            check_url("privacy.reachable", it.get("privacy_url"), a.offline)
    else:
        privacy = check_url("privacy.reachable", it.get("privacy_url"), a.offline)
    if privacy is not None:
        if len(privacy) < 800 and not a.privacy_text:
            out("WARN", "privacy.length", f"only {len(privacy)} characters of text; page may render with JS. Re-run with --privacy-text")
        else:
            if "회원가입" in norm(privacy) or "회원 가입" in privacy:
                out("PASS", "privacy.purpose_signup", "mentions 회원가입")
            else:
                out("FAIL", "privacy.purpose_signup", "does not state 회원가입 as the purpose (rejection: 소셜 로그인 수집 목적)")
            if "카카오" in privacy:
                out("PASS", "privacy.kakao", "mentions 카카오")
            else:
                out("FAIL", "privacy.kakao", "does not mention data received through 카카오 (Kakao Sync policy)")
            for m in re.finditer(r"(주식회사\s*)?카카오(?!톡|계정|\s*로그인|\s*싱크)", privacy):
                ctx = privacy[max(0, m.start() - 60): m.end() + 60]
                if re.search(r"위탁|수탁", ctx) and not re.search(r"알림톡|딜러|빼고|제외|아니|아닙|않", ctx):
                    out("WARN", "privacy.kakao_processor", f"Kakao may be listed as a processor (위탁): '…{ctx.strip()}…'. Kakao Login is not 위탁; remove it (DevTalk 148755/3)")
                    break
            for sid in sorted(scope_ids):
                kws = SCOPE_KEYWORDS.get(sid, [])
                hit = next((k for k in kws if k.lower() in privacy.lower()), None)
                level = "WARN" if sid == "plusfriends" else "FAIL"
                if hit:
                    out("PASS", f"privacy.item.{sid}", f"found '{hit}'")
                else:
                    out(level, f"privacy.item.{sid}", f"{SCOPE_LABEL.get(sid, sid)} not found (rejection: 소셜 로그인 개인정보 처리방침)")
            has_opt = any(s.get("level") == "optional" for s in scopes)
            if "필수" not in privacy:
                out("FAIL", "privacy.required_marked", "no '필수' marking (rejection: 개인정보 수집 조건 미표기)")
            else:
                out("PASS", "privacy.required_marked", "has '필수' marking; confirm each item's condition by eye")
            if has_opt and "선택" not in privacy:
                out("FAIL", "privacy.optional_marked", "optional items requested but no '선택' marking")
            elif has_opt:
                out("PASS", "privacy.optional_marked", "has '선택' marking")

    # --- Service terms ---------------------------------------------------------
    pv = (it.get("privacy_url") or "").rstrip("/")
    for t in terms:
        if pv and (t.get("url") or "").rstrip("/") == pv and not re.search(r"개인정보", t.get("title_ko", "")):
            out("FAIL", "privacy.url_is_terms", f"privacy_url equals the URL of term '{t.get('title_ko')}'; the form needs the privacy policy, not the terms of service (DevTalk 150043/7)")
    tags = [t.get("tag", "") for t in terms]
    if len(set(tags)) != len(tags):
        out("FAIL", "terms.tag_unique", f"duplicate tags: {tags}")
    if not any(t.get("required") for t in terms):
        out("FAIL", "terms.required_present", "no 필수 term; 간편가입 needs at least one active term")
    for t in terms:
        tag = t.get("tag", "")
        tk, te = t.get("title_ko", ""), t.get("title_en", "")
        cid = f"terms.{tag or '?'}"
        if not TAG_RE.match(tag):
            out("FAIL", cid + ".tag", f"tag '{tag}' must use only letters, digits, - and _")
        if not tk or len(tk) > 45:
            out("FAIL", cid + ".title_ko", f"Korean title empty or over 45 characters ({len(tk)})")
        odd = sorted({c for c in tk if not (re.match(r"[가-힣A-Za-z0-9 ]", c) or 33 <= ord(c) <= 126)})
        if odd:
            out("WARN", cid + ".title_ko_chars", f"characters outside Hangul/keyboard set: {''.join(odd)} (the console accepted '·' in a live app's term title)")
        if not te or len(te) > 100 or any(ord(c) > 126 for c in te):
            out("FAIL", cid + ".title_en", "English title missing, over 100 characters, or not ASCII")
        url = t.get("url")
        if t.get("required") and not url:
            out("FAIL", cid + ".url", "required term has no URL")
        text = None
        if tag in term_text_override:
            text = read_file(term_text_override[tag])
        elif url:
            text = check_url(cid + ".url", url, a.offline)

        is_ad = any(h in tk for h in AD_HINTS)
        if is_ad:
            if not ("광고성정보수신" in norm(tk)):
                out("FAIL", cid + ".ad_title", f"ad term title must say '광고성 정보 수신 동의' (KISA guide); got '{tk}'")
            banned = next((b for b in BANNED_AD_TITLES if norm(b) in norm(tk)), None)
            if banned:
                out("FAIL", cid + ".ad_banned", f"'{banned}' is not explicit consent under the KISA guide")
            if t.get("required"):
                out("FAIL", cid + ".ad_optional", "ad consent must be 선택 동의, not 필수")
            if not url:
                out("FAIL", cid + ".ad_url", "ad consent term has no URL; the term page must be live before registering")
            if text is not None:
                if len(text) < 200:
                    out("WARN", cid + ".ad_page", "term page text is short; check it in ego-browser or pass --term-text")
                elif "광고성 정보" not in text and "광고성정보" not in norm(text):
                    out("FAIL", cid + ".ad_page", "term page does not contain '광고성 정보'")
                else:
                    out("PASS", cid + ".ad_page", "term page mentions 광고성 정보")
            if not any(k in tk for k in ["카카오톡", "문자", "이메일", "SMS", "푸시", "전화"]):
                out("WARN", cid + ".ad_media", "title names no medium; KISA recommends naming the media (카카오톡·문자·이메일)")
        elif any(norm(b) in norm(tk) for b in BANNED_AD_TITLES):
            out("FAIL", cid + ".ad_banned", f"'{tk}' looks like ad consent with a banned title")

    n_fail = results.count("FAIL")
    n_warn = results.count("WARN")
    n_pass = results.count("PASS")
    print(f"\nSummary: PASS {n_pass}  WARN {n_warn}  FAIL {n_fail}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
