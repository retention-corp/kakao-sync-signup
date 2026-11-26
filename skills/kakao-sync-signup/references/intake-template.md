# Intake (one message, at the start)

Collect every value, file and approval the run needs before the browser opens. The person should
not meet a new request halfway through: the skill already knows what Kakao will ask for. Pre-fill
what you can, then ask only for the rest. Keep the filled intake in the service's own repo or a
private folder, never in this skill repo: it holds business data.

Why one round: in the 2026-11-25 real run, the agent stopped three times for things it could have
asked at the start (the business certificate, the legal-page host, a Cloudflare login). Each stop
cost the person a context switch.

## 1. What to collect

### A. Accounts (check yourself first, ask only if unknown)

| # | Item | How to check | Why |
|---|---|---|---|
| A1 | Kakao Developers login works in the browser | Open `/console/app` read-only | Every console step |
| A2 | Role on the app: Owner or Editor | Console > 앱 > 멤버 | Biz app conversion needs Owner |
| A3 | Kakao Business login (partner center) works | Open `https://business.kakao.com/profiles` read-only | Channel creation and review |
| A4 | Role on an existing channel: 마스터 or 매니저 | Kakao Business channel list | Channel link needs it |
| A5 | Hosting/DNS access for legal pages, if the agent will deploy them | CLI login (`wrangler whoami`, `vercel whoami`) | Phase 2 deploy |

If a login is missing, put it in the human timeline (section 3) as the first item, not as a later
surprise.

### B. Business and documents

| # | Item | Pre-fill from | Notes |
|---|---|---|---|
| B1 | 상호, 사업자등록번호, 대표자 | Site footer, Kakao Business record (the biz-app dialog loads it) | 회사명 in the app must equal 상호 |
| B2 | Applicant type for the channel review: 대표자 / 직원 / 대행사 | Ask | Decides the documents |
| B3 | Business registration certificate (사업자등록증 or 고유번호증), JPG/PNG/PDF, 10 MB max | Ask for a file path | Mask 주민등록번호 뒷자리, 전화번호, 이메일 before upload. The agent scans it |
| B4 | 직원: 재직 증빙. 대행사: 업무 대행 계약서 or 위임장 + 대행사 사업자등록증 | Ask only for that type | Kakao Business guide 2-2 |
| B5 | Industry license (업종별 인허가 서류) if the business needs one | Ask | Food, medical, lodging, education services, alcohol, tobacco |
| B5a | Licensed 업종 printed on the certificate (예: 부동산업 → 중개사무소 개설 등록증) and whether this channel operates in it | Read the certificate, then ask | The review wizard asks "해당 업종으로 운영할 계획이 없어요" or "인허가 서류를 제출할게요". Pick the first only when true |
| B6 | Phone that can receive a KakaoTalk 전자증명서 / 대표자 휴대폰 인증 | Ask who holds it | The one step only the person can do |

### C. Service

| # | Item | Pre-fill from | Default |
|---|---|---|---|
| C1 | Service name (= app name, shown on the consent screen) | Site title | — |
| C2 | App icon 128x128 (JPG/GIF/PNG, 250 KB) and channel profile image 640x640 | Site favicon/logo | Agent can draw one from the logo; ask |
| C3 | App category | Service type | 예: 생산성/도구 |
| C4 | Domain, sign-up URL, redirect URI(s) | Repo routes, env | `https://<domain>/auth/kakao/callback` |
| C5 | Own sign-up form besides Kakao? | Repo, live site | Decides how Kakao reviews (`review-checklist.md` 12a) |
| C6 | Under-14 users possible? | Audience | No → add 만 14세 이상 연령 동의 |
| C7 | Data stored or processed abroad (hosting, email/SMS vendors)? | Infra | Fill 개인정보 국외이전 if yes |
| C8 | Withdrawal path that calls unlink exists? | Repo | Required before review |
| C9 | Is the service formally launched (open to the public, not CBT/OBT, site complete), with real sign-up, log-in and withdrawal? | Ask; check the live site | Not launched → no business channel review, no consent-item review, no 간편가입 in the live app. Run the test-app path only. Kakao Business rejects pre-launch services ("정식 사업 미개시") |

### D. Legal pages

| # | Item | Default |
|---|---|---|
| D1 | Terms of service URL | Ask; or agent drafts |
| D2 | Privacy policy URL | Ask; or agent drafts with every Kakao item, 필수/선택, purpose 회원가입, Kakao not a processor |
| D3 | Ad-consent page URL (if marketing messages) | Agent drafts per `ad-consent-rules.md` |
| D4 | If the agent drafts: where to host, and permission to deploy | Own subdomain. Not a blog, shared domain or GitHub Pages |
| D5 | Withdrawal path and deletion policy: what is deleted, what is kept (예: 주문 기록 5년), how the Kakao member ID is removed | Ask. Needed for the unlink webhook (`api-readback.md` 5). If none exists, the webhook waits for this decision |

### E. Consent items, terms and channel

| # | Item | Default |
|---|---|---|
| E1 | Items, level, purpose | 이메일·이름·전화번호 필수; 성별·출생 연도 선택 only if used; 채널 추가 선택 |
| E2 | Terms and tags | `terms_<YYYYMMDD>` 필수, `privacy_<YYYYMMDD>` 필수, `ad_consent_<YYYYMMDD>` 선택 |
| E3 | Ad media | 카카오톡·문자·이메일 |
| E4 | Channel: new or existing (required for 간편가입) | Existing only if not linked to another app |
| E5 | New channel name and **검색용 ID (can never change)** | Service name |
| E6 | Text explaining why the channel name differs from 상호 (사업자정보 불일치 소명, under 300 chars) | Agent drafts. Allowed characters: 한글, 영문, 숫자, ( ) & . , - ~ / and spaces. No colon, so no URL; put the URL in the separate [링크] field |

### T. Test app (ask; explain first)

Explain in two sentences, then ask yes/no:

> 테스트 앱은 실제 앱과 따로 있는 연습용 앱이에요. 카카오 심사 없이 이름·전화번호까지 받는 동의 화면을
> 앱 멤버에게만 미리 띄워 볼 수 있어서, 심사 전에 화면을 확인하거나 아직 출시 전인 서비스를 시험할 때 써요.

Recommend yes when: the service is pre-launch, or the consent-item review is not approved yet, or
the user wants to test the real login without touching live users. Recommend no when: the live app
already has all permissions and a test login is not needed. A test app also needs a developer
channel (created in Kakao Business, then made public) if the consent screen should show channel-add.

### G. Approvals (one line each)

1. Create app `<name>` (only if new).
2. Save settings in app `<id/name>` (and test app, if T = yes).
3. Create channel `<name>` with 검색용 ID `<id>`; create developer channel `<name>` and make it public (if T = yes).
4. Upload the provided documents and submit the business-channel review.
5. Submit the app-channel link request.
6. Submit the 개인정보 동의항목 review (only for a live service).
7. Draft and deploy legal pages to `<host>` (if D4).

## 2. Korean message to send

Send this once. Replace `{…}`. Mark pre-filled rows "확인만".

```text
카카오싱크 설정에 필요한 걸 한 번에 여쭤볼게요. "확인만"은 제가 찾은 값이에요. 틀린 줄만 고쳐 주세요.

[서비스]
1. 서비스 이름: {이름} — 확인만
2. 도메인/가입 페이지: {URL} — 확인만
3. 지금 실제 회원이 있나요, 출시 전인가요? {추정}
4. 카카오 말고 자체 가입 양식이 있나요? {찾은 것}
5. 만 14세 미만도 가입하나요? 추천: 아니오 → "만 14세 이상 연령 동의" 추가
6. 고객 정보를 해외 서버에 두나요? {추정}

[사업자·서류]
7. 상호/사업자등록번호/대표자: {값} — 확인만
8. 채널 심사 신청인: 대표자 / 직원 / 대행사
9. 사업자등록증 파일 경로(주민번호 뒷자리·연락처 가린 것): ________
   (직원이면 재직 증빙, 대행사면 위임장도 / 인허가 업종이면 인허가 서류도)
10. 카카오톡 전자증명서·휴대폰 인증을 받을 사람: ________

[받을 정보와 약관]
11. 받을 정보: 이메일·이름·전화번호(필수), 채널 추가(선택) — 추천대로 갈까요?
12. 약관: 이용약관·개인정보처리방침(필수), 광고성 정보 수신 동의(선택, 카카오톡·문자·이메일)
13. 약관 페이지: 있는 주소 {URL} / 없으면 제가 써서 {추천 주소}에 올려도 될까요?

[채널]
14. 채널: 새로 만들기 / 기존 {@ID} 연결 (채널 하나는 앱 하나에만 연결돼요)
15. 새 채널 이름 {추천}, 검색용 ID {추천} — 검색용 ID는 나중에 못 바꿔요

[테스트 앱]
16. 테스트 앱을 만들까요? (설명: {T의 두 문장}) 추천: {예/아니오, 이유}

[승인 — 예/아니오]
17. 앱 {이름} 만들기·설정 저장
18. 채널 {이름} 만들기 + 서류 올리고 비즈니스 심사 신청
19. 앱-채널 연결 신청 (심사 영업일 3~5일)
20. 개인정보 동의항목 심사 신청 (실제 서비스일 때만)
21. 약관 페이지 작성·배포 ({주소})

[직접 하실 순간 — 미리 알려 드려요]
- 카카오/클라우드 로그인이 풀려 있으면 로그인 1분 ({해당 여부})
- 채널 심사: 카카오톡 전자증명서 또는 휴대폰 인증 3분
- (테스트 앱) 실제 로그인 시험에서 [동의하고 계속하기] 1분
그 외는 제가 하고, 심사 결과가 나오면 이어서 진행해요.
```

## 3. Human timeline (include in the message)

List each moment the person will be needed, in order, with minutes. Typical:

1. Login fixes found in section A (1 min each).
2. Channel review phone verification (3 min). Documents are uploaded by the agent.
3. Real login test in the test app (1 min), if T = yes.
4. Nothing else unless a review is rejected.

## 4. JSON for `scripts/precheck.py`

Write the confirmed values to `<service-repo>/.kakao-sync/intake.json` and add that folder to
`.gitignore`. Example (fictional product from the 2026-11-25 run):

```json
{
  "service_name": "auto-fde",
  "app_id": 1665131,
  "test_app_id": 1665134,
  "company_name": "리텐션 주식회사",
  "site_url": "https://auto-fde.retn.kr/",
  "signup_url": "https://auto-fde.retn.kr/",
  "privacy_url": "https://auto-fde.retn.kr/privacy/",
  "redirect_uris": ["https://auto-fde.retn.kr/auth/kakao/callback"],
  "own_identity_verification": false,
  "own_signup_form": false,
  "channel_public_id": "_iaevX",
  "scopes": [
    {"id": "account_email", "level": "required", "purpose": "회원가입, 플레이북 실행 결과 안내"},
    {"id": "name", "level": "required", "purpose": "회원가입, 작업 담당자 표시"},
    {"id": "phone_number", "level": "required", "purpose": "회원가입, 사람 단계 요청 연락"},
    {"id": "plusfriends", "level": "optional", "purpose": "카카오톡 채널 소식 안내"}
  ],
  "terms": [
    {"title_ko": "auto-fde 이용약관", "title_en": "auto-fde Terms of Service", "url": "https://auto-fde.retn.kr/terms/", "required": true, "tag": "terms_20261125"},
    {"title_ko": "개인정보처리방침", "title_en": "Privacy Policy", "url": "https://auto-fde.retn.kr/privacy/", "required": true, "tag": "privacy_20261125"},
    {"title_ko": "광고성 정보 수신 동의(카카오톡·문자·이메일)", "title_en": "Consent to receive advertising information (KakaoTalk, SMS, email)", "url": "https://auto-fde.retn.kr/terms/ad-consent/", "required": false, "tag": "ad_consent_20261125"}
  ]
}
```

Optional field `business_number`: when set, the script checks that the site shows it.
`level` is `required`, `optional` or `on_demand` (이용 중 동의). Scope IDs are the console IDs:
`profile_nickname`, `profile_image`, `account_email`, `name`, `gender`, `age_range`, `birthday`,
`birthyear`, `phone_number`, `account_ci`, `shipping_address`, `plusfriends`.
Source: https://developers.kakao.com/docs/latest/ko/kakaologin/utilize#scope-user
