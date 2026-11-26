# Console steps

Menu paths and labels were read from the live console on 2026-11-24 (a live app, read-only). Console base: `https://developers.kakao.com/console/app/<APP_ID>`.

Sources:
- Kakao Sync setup: https://developers.kakao.com/docs/latest/ko/kakaosync/prerequisite
- Kakao Login setup: https://developers.kakao.com/docs/latest/ko/kakaologin/prerequisite
- App settings: https://developers.kakao.com/docs/latest/ko/app-setting/app

## Contents

1. Console map
2. Read-only survey
3. Setup steps 0-11
4. What triggers a human review
5. Safe and unsafe clicks
6. Test app path (pre-launch or demo services)
7. Console quirks (tested 2026-11-25)

Scripts: `scripts/console-helpers.mjs` (exact-ID scope dialogs, term adding, app-ID guard),
`scripts/clean-shot.mjs` (safe screenshots), `scripts/scan-shots.swift` (OCR leak scan).

## 1. Console map

| Menu (as shown) | URL path | What lives there |
|---|---|---|
| 앱 > 일반 | `/config` | 앱 기본 정보 (icon, 앱 이름, 회사명, 카테고리, 앱 대표 도메인), 비즈니스 정보, 테스트 앱 |
| 앱 > 플랫폼 키 | `/config/platform-key` | REST API 키 (로그인 리다이렉트 URI, 클라이언트 시크릿), JavaScript 키 (JavaScript SDK 도메인), 네이티브 앱 키 |
| 앱 > 제품 링크 관리 | `/config/product-link` | 웹 도메인 for links inside Kakao messages and shares. Not needed for login |
| 앱 > 추가 기능 신청 | `/config/review` | 신청 자격 확인, 비즈니스 정보, 개인정보 동의항목, 카카오톡 채널 연결 |
| 앱 > 카카오톡 채널 | `/config/channel` | 연결된 카카오톡 채널, 대표 채널 |
| 앱 > 웹훅 | `/config/webhook` | 계정 상태 변경 웹훅, 연결 해제 웹훅, 카카오톡 채널 웹훅 |
| 앱 > 멤버 | `/config/member` | Owner / Editor roles |
| 카카오 로그인 > 일반 | `/product/login` | 사용 설정 ON/OFF, OpenID Connect |
| 카카오 로그인 > 동의항목 | `/product/login/scope` | 개인정보 and 접근권한 items, 대표 채널, 개인정보 국외이전, 동의 화면 미리보기 |
| 카카오 로그인 > 간편가입 | `/product/login/simple-signup` | 사용 설정, 서비스 약관 추가, 만 14세 이상 연령 동의 추가, 동의 화면 미리보기 |
| 카카오 로그인 > 고급 | `/product/login/advanced` | 카카오싱크 플러그인, 로그아웃 리다이렉트 URI, 사용자 아이디 고정 |

There is no separate "web platform" menu any more. A REST-API login needs only the
redirect URI on the REST API key. A JavaScript SDK login also needs the JavaScript SDK
domain on the JavaScript key.

## 2. Read-only survey

Run this before the intake. Extract page text with `page.evaluate(() => document.querySelector('main').innerText)`.
Mask any 24+ character hex or token string before you save or print it.

1. `/config`: app name, company name, category, icon present, biz app or not.
2. `/config/review`: status of 신청 자격 확인, 비즈니스 정보, 개인정보 동의항목, 카카오톡 채널 연결.
   If a row says 반려, click its "확인" button to read the reason. It only opens a dialog.
3. `/config/channel`: linked channels and 대표 채널.
4. `/product/login`: 사용 설정 state.
5. `/product/login/scope`: each item's state. "권한 없음" means the review has not granted it.
6. `/product/login/simple-signup`: 사용 설정 and every term's title, URL, tag, required or optional.
7. `/config/webhook`: whether 연결 해제 웹훅 or 계정 상태 변경 웹훅 is registered.
8. `/config/member`: your role. Biz app conversion needs Owner.

Do not open the REST API key detail page in this survey. It shows the key.

## 3. Setup steps

Each step lists who acts, and whether Kakao reviews it.

### Step 0. Create the app (new service only)

- Where: `/console/app` > [앱 생성]. Only when the service has no Kakao app yet.
- Fields (seen 2026-11-25): 앱 아이콘 (JPG/GIF/PNG, 128 px recommended, 250 KB max), 앱 이름 (필수),
  회사명 (필수, "사업자 정보와 동일한 상호"), 카테고리 (필수, dropdown), 앱 대표 도메인 (optional), and one
  checkbox confirming the app breaks no 운영정책 category, content or activity rule.
- Upload the icon here: biz app conversion later needs it.
- The category list scrolls inside the dialog; scroll the option into view before clicking.
- Note the new app ID and check it in the URL before every later write (`assertApp`).

### Step 1. App basic info

- Where: 앱 > 일반 > 앱 기본 정보 > 수정.
- Set the icon, 앱 이름, 회사명 to match the real service. These show on the consent screen.
- Rule: icon under 250 KB, 128x128 px or smaller recommended.
- Reviewers reject a mismatch ("비즈 앱 정보 수정 필요"). Source: kakaologin/faq#reject-reason.

### Step 2. Biz app conversion

- Where: 앱 > 일반 > 비즈니스 정보 > 사업자 정보 등록.
- Who: the app Owner only. The app must have an icon.
- Review: none. "별도 심사는 필요하지 않습니다." (kakaosync/prerequisite)
- The business registration number must equal the one on the business channel.
- Seen 2026-11-25: the dialog first asks 사업자 구분 and the number (three fields). [확인] then loads the
  company record from Kakao Business: 회사명, 대표자명, 업태, 종목, 우편번호, 주소. If 회사명 differs from the
  app's 회사명, the dialog asks you to change the app name to match. Tick "위 내용을 모두 확인하였으며,
  이에 동의합니다." (scroll it into view first) and save. Never screenshot this second screen unmasked:
  it shows the representative's name and the company address.
- 테스트 앱 can only be created after this conversion.

### Step 3. 신청 자격 확인

- Where: 앱 > 추가 기능 신청 > 신청 자격 확인.
- Needs: Owner or Editor, the account's identity verification (본인인증), biz app.
- If 본인인증 is missing, hand off (Kakao account settings > 본인인증).

### Step 4. Business channel

- See `channel-steps.md`. The channel must be a 비즈니스 채널 with the same business
  number, not linked to any other app, and you need 마스터 or 매니저 on it.

### Step 5. 카카오톡 채널 연결

- Where: 앱 > 추가 기능 신청 > 추가 기능 > 카카오톡 채널 연결 > 신청.
- Pick the channel from the list. Kakao reviews it, 3-5 business days.
- The list hides channels that fail any condition in `channel-steps.md`.

### Step 6. 비즈니스 정보

- Where: 앱 > 추가 기능 신청 > 비즈니스 정보 > 신청.
- "비즈 앱과 비즈 채널이 연결된 앱은 비즈니스 정보의 [신청]을 선택하면 자동으로 심사가
  승인됩니다." (kakaosync/prerequisite). A pending business-info review older than 30 days
  auto-rejects the consent-item request (kakaologin/faq).

### Step 7. Kakao Login ON and redirect URI

- Where: 카카오 로그인 > 일반 > 사용 설정 > 상태 ON. OFF gives KOE004.
- Redirect URI: 앱 > 플랫폼 키 > REST API 키 (select the key the service uses) >
  카카오 로그인 리다이렉트 URI, then 저장.
- Rules (app-setting/app#redirect-uri): up to 10; http and https are separate entries;
  the request's `redirect_uri` must match exactly, trailing slash included; mismatch
  gives KOE006. The doc says the path cannot carry arbitrary parameters.
- The REST API key has client secret ON by default. Token requests must send
  `client_secret`.
- This page shows the REST API key and the client secret in clear text. Read it only through
  `H.safeSnapshot(page)` or `H.safeText(page)` from `console-helpers.mjs`; never print a raw
  `page.snapshot()` or body text here. Do not read the client secret at all unless the service's
  server env needs it. Then move it without printing (the same pattern works for the admin key on
  앱 > 어드민 키):
  1. In the browser script, read the value inside `page.evaluate` and print one marker line,
     `KEY=<value>`.
  2. In the shell, capture that output in a variable: `OUT=$(ego-browser nodejs <<'EOF' … EOF)`,
     then `V=$(printf '%s\n' "$OUT" | sed -n 's/^KEY=//p')`. Print only `${#V}`.
  3. Pipe it straight to the store: `printf %s "$V" | vercel env add NAME production` (or the
     host's equivalent), and the password manager. `unset V` at the end.

### Step 8. 대표 채널

- Where: 카카오 로그인 > 동의항목 > 대표 채널 (also shown on 앱 > 카카오톡 채널).
- Without it the consent screen has no 카카오톡 채널 추가 line. (kakaosync/prerequisite)
- The channel must be public. A new channel is private by default; picking it shows "비공개이거나
  제재되어 사용할 수 없는 상태입니다." Turn on 공개 in Kakao Business (channel dashboard > [공개 설정하기])
  first. Seen 2026-11-25.
- The "대표 채널 선택" link on 앱 > 카카오톡 채널 leads to this same 동의항목 section.

### Step 9. Service terms and 간편가입

- Where: 카카오 로그인 > 간편가입 > 서비스 약관 추가.
- Fields (kakaologin/prerequisite#service-terms):
  - 한글 제목: Korean, English, digits, spaces, keyboard symbols, max 45 characters.
  - 영문 제목: required even without an English page, max 100 characters.
  - URL: required for required terms. Optional terms may omit it, but the ad-consent term
    must have a live page (see `ad-consent-rules.md`).
  - 동의 단계: 필수 동의 or 선택 동의.
  - 태그: letters, digits, `-`, `_` only. Recommended `<keyword>_<YYYYMMDD>`. The app reads
    consent by this tag, so it must match the code.
- New terms land under "비활성 서비스 약관" with 사용 설정 OFF. Turn each ON (confirm "서비스 약관을
  활성화하시겠습니까?"). Then 간편가입 > 사용 설정 > ON (confirm "간편가입을 활성화 하시겠습니까?"). At
  least one active term is required.
- The console did not check that the term URL opens (seen in a test app, 2026-11-25; not tried on an
  original app). `precheck.py` must check it either way.
- Consider 만 14세 이상 연령 동의 추가 if the service does not handle guardian consent
  for users under 14.
- Kakao shows this warning on the page: a term that does not match the service, or that
  breaks the law or government guides, can restrict the service.

### Step 10. 개인정보 동의항목 request

- Where: 앱 > 추가 기능 신청 > 추가 기능 > 개인정보 동의항목 > 신청.
- Form (kakaologin/prerequisite#additional-features):
  - [A] 개인정보: each item and its level. At least one must be 필수 or 선택.
  - [B] 카카오 로그인 이용 동의 checkbox, then 다음.
  - [C] 회원가입 링크: the sign-up page URL (app store URL for a native app).
  - [D] 개인정보 처리방침 URL.
  - [E] 회원가입 화면: ONE file, JPG/JPEG/PNG/PDF, 20 MB or less. Build it with
    `evidence-pack.md`.
  - [F] 수집 사유: the purpose of each item.
- Review: 3-5 business days. Result by email to app members and on this page.
- Run `review-checklist.md` and `scripts/precheck.py` first. The submit click needs the
  write grant from the intake.

### Step 11. After approval

- Where: 카카오 로그인 > 동의항목 > each item > 설정.
- Set 동의 단계 and 동의 목적 (required field). Use the same purpose text as the request.
- 카카오계정으로 수집 후 제공: turn on for items that must not be empty (not available
  for phone_number).
- plusfriends: 선택 동의 recommended. Only available after a channel is linked.
- Open 동의 화면 미리보기 on the 간편가입 page. Mask the email, then screenshot it.
- Lowering a level (필수 to 선택) or turning an item off applies at once, no review.

## 4. What triggers a human review

| Action | Reviewer | Time | Source |
|---|---|---|---|
| Biz app conversion | none | instant | kakaosync/prerequisite |
| 비즈니스 채널 conversion | Kakao Business partner center | 3-5 business days | kakaotalk-channel/common |
| 카카오톡 채널 연결 | Kakao Developers | 3-5 business days | kakaotalk-channel/common |
| 비즈니스 정보 (with linked channel) | none | auto-approved | kakaosync/prerequisite |
| 개인정보 동의항목 | Kakao Developers | 3-5 business days | kakaologin/prerequisite |
| 간편가입 ON, terms | none | instant | kakaologin/prerequisite |

## 5. Safe and unsafe clicks

Safe in any app: menu links, the "확인" buttons in the 심사 사유 column, 동의 화면 미리보기,
the dialog's 닫기 button.

Unsafe without the write grant: every toggle (they can save at once), 수정, 삭제, 저장,
신청, 연결 해제, 순서 변경, 서비스 약관 추가, 테스트 앱 생성, 앱 영구 삭제, and the
"더보기" menu on a key (it holds edit and delete).

## 6. Test app path (pre-launch or demo services)

Use this when the service is not live yet, or to show the full consent screen before any review.
Create the test app only after the user answered yes to intake item T (what it is, why it helps,
and that it needs a developer channel made public if channel-add should show).
Tested on auto-fde 2026-11-25 (original 1665131, test app 1665134).

1. Original app must be a biz app first. Then 앱 > 일반 > 테스트 앱 > [테스트 앱 생성] (default name
   "<app>-TEST"). Up to 5 per original app. Members and owner copy from the original.
2. In the test app, 카카오 로그인 is OFF by default. Turn it ON.
   The test app has its own keys: add the Redirect URI to its REST API key too, or a real
   login test fails with KOE006 (seen 2026-11-25).
3. Consent items: name, gender, birth year, phone and others are settable without review (test-app
   permission, members only). plusfriends shows 권한 없음 until a channel is linked. CI stays 권한 없음
   even with a channel ((it needs its own review; a live app with a linked channel shows the same)).
4. 신청 자격 확인 is separate for the test app. Do it again.
5. Channel: test apps can only request 카카오톡 채널 연결/해제, and the link is instant. Link a
   **developer channel** only (Kakao Business > 내 비즈니스 > [개발자용 채널 만들기]). Never link a live
   business channel to a test app: it then cannot link to the live app (DevTalk 142570/18).
6. Make the developer channel public, set it as 대표 채널, then set plusfriends.
7. Add terms, turn them ON, turn 간편가입 ON. Open 동의 화면 미리보기 for the full screen.

The test app proves the consent screen. It does not replace the live app's reviews.

## 7. Console quirks (tested 2026-11-25)

- Dialogs and dropdowns scroll on their own. Call `scrollIntoView({block:"center"})` on the target
  (category option, agreement checkbox, 저장 button) before clicking, or the click fails with
  "element is not visible in the viewport".
- A floating 맨 위로 button (`#float_btn`) covers controls near the bottom right. Center the control first.
- Find consent rows by the exact ID cell. "name" also matches "profile_nickname".
- Choosing 필수 동의 reveals a 카카오계정으로 수집 후 제공 switch (`button[value=on]`). Not offered for phone.
- The REST API key page shows the client secret in clear text. Use `clean-shot.mjs` for pictures
  and `H.safeSnapshot` / `H.safeText` for reading (Step 7).
- Kakao Business (partner center) renders inside shadow DOM, and its wizards are same-origin iframes
  (`/wizard/partner?...`). `document.body.innerText` returns almost nothing; use the snapshot tree or walk
  shadow roots. `page.fill` may refuse Korean in its inputs; type English, or click and use the keyboard.
