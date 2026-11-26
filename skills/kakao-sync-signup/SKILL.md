---
name: kakao-sync-signup
description: >-
  Set up Kakao Sync (카카오싱크 간편가입) for a Korean web service by driving the Kakao
  Developers console and Kakao Business in the user's signed-in browser: app creation, biz app
  conversion, business Kakao Channel (카카오톡 채널, 플친) creation and linking, consent items
  (이름, 전화번호, 이메일, 성별, 출생 연도, 채널 추가), service terms with an optional 광고성 정보
  수신 동의, 간편가입 ON, and Kakao reviews prepared so they pass on the first try. Asks for every
  value and document once at the start, so the person is only needed for login, phone
  verification and approvals. Use this whenever the user says "카카오싱크 붙여줘", "카카오 간편가입",
  "카카오 로그인으로 전화번호 받기", "동의항목 심사", "플친 추가 동의", "카카오톡 채널 연결",
  "광고성 정보 수신 동의 약관", or wants Kakao sign-up for a service, even if "Kakao Sync" is not said.
---

# Kakao Sync sign-up

This skill sets up Kakao Sync for one service so that one Kakao sign-up gives the service a
verified name, phone number, email, ad consent and (optionally) a channel friend. The agent
does the console work. The person acts only where Kakao requires a person.

Facts were checked against the official docs on 2026-11-24 and in a real run on 2026-11-25
(`docs/build-log/2026-11-25-auto-fde.md` in this repo). Each reference file cites its sources.
If the console looks different, trust the live console and the docs, then update the file.

## Rules that do not bend

- **One intake, at the start.** Ask for every value, file and approval the whole run needs in ONE
  message before the browser opens (Phase 1). Do not discover a needed document or decision
  halfway and stop there; the skill already knows what Kakao will ask for. Later questions are
  only for things that could not be known at the start (예: a rejection reason).
- **Approvals.** Do not create, save, toggle, delete or submit anything in a Kakao app, test app or
  channel until the intake reply grants it for that exact app or channel. Reading and the "확인"
  (view) dialogs are always allowed.
- **Test app only with consent.** Explain what a test app is for (intake item T) and create it only
  when the user says yes.
- **Irreversible values.** A channel's 검색용 ID and a developer channel's name can never change.
  Confirm them in the intake, not during the run.
- **Secrets.** Never put the REST API key, client secret or admin key in a screenshot, report,
  repo or your own context. On key pages (앱 > 플랫폼 키, 앱 > 어드민 키) read only through
  `safeSnapshot` / `safeText` in `scripts/console-helpers.mjs`, which mask key-like strings. When a
  server env needs a key, move it shell-to-store without printing (`console-steps.md` Step 7).
  Do not open a key page unless the step needs it.
- **Personal data.** Kakao rejects any evidence or document with unmasked personal data. Mask with
  the tested methods in `references/evidence-pack.md`, scan with `scripts/scan-shots.swift`, and
  look at each image once.
- **A business channel is required.** 간편가입 needs a business channel linked to the app. One
  channel links to one app only. Only the channel-add line (`plusfriends`) is optional.
- **Launched services only.** Kakao Business rejects the business channel review for a service that
  has not formally launched: "[전환 불가-정식 사업 미개시] 정식 사업 시작 후 신청 가능 (CBT, OBT, 사이트
  미완성 시 전환 불가)" (rejection received 2026-11-26 for a pre-launch service). No business
  channel means no channel link and no 간편가입 in the live app. So when intake C9 says
  pre-launch, beta or incomplete site: stop the live-app path after Step 7 (Redirect URI), run
  the test-app path only, and tell the user to come back when the service is open to the public.
  Do not submit the channel review to "try"; a rejection costs 3-5 business days, and the
  documents are destroyed 30 days after a rejection.
- **One app per service.** If the service already uses Kakao Login, use that app. A new app gives
  existing users a new member ID. Source: https://developers.kakao.com/docs/latest/ko/kakaosync/faq
- **Truthful reviews only.** Do not submit the 개인정보 동의항목 review for a service with no real
  sign-up, log-in and withdrawal. The eligibility check makes the applicant confirm "제출하는 모든
  정보는 사실과 일치합니다". For a pre-launch service, show the full consent screen in a test app.
- **Screenshots.** Take console screenshots with `scripts/clean-shot.mjs`, then run
  `swift scripts/scan-shots.swift <folder> --deny "<names to hide>"` before sharing or committing.
- **Language.** Talk to the user in Korean. Hand-offs use `references/handoffs-ko.md`.

## Workflow

Record progress after each phase in a handoff note (see "Handoff note"). Kakao reviews take
3-5 business days, so a run almost always spans sessions.

### Phase 1. One intake (no browser writes)

1. Read `references/intake-template.md`. It lists every value, file and approval, where to look
   first, and the Korean message to send.
2. Pre-fill what you can find yourself: the service repo, the live site footer and policy pages,
   and the console in read-only mode (`references/console-steps.md` "Read-only survey").
   If 간편가입 is already ON, switch to audit mode: run Phase 3 on the live setup, report the gaps,
   change nothing without a grant.
3. Run `scripts/precheck.py` on the pre-filled values. Turn every FAIL into a proposed fix or a
   question in the intake.
4. Send the Korean intake in ONE message. It includes:
   - pre-filled values to confirm,
   - questions with your recommendation,
   - the files to provide (예: masked business registration certificate),
   - the test-app question with its explanation,
   - the approvals list,
   - a timeline of the few moments the person will be needed, with minutes for each.
5. When files arrive, check them before the run: `swift scripts/scan-shots.swift <file> --deny ...`
   (it flags 주민등록번호, phone, email). Convert a PDF page to PNG first (`sips -s format png`).

### Phase 2. Make the website ready

Kakao reviews the live site, not the console. Before any submit the site must show:

1. A sign-up path with a visible Kakao login button and the service name.
2. A privacy policy naming each Kakao item with 필수/선택, the purpose 회원가입, and that the data
   comes from Kakao (Kakao is not a processor).
3. A withdrawal path that calls the Kakao unlink API.
4. One live page per service term, including the ad-consent page.
5. The company name and business number in the footer, identical to the app.

If pages are missing and the user approved it in the intake, draft them in the service repo and
deploy through that repo's own process.

### Phase 3. Pre-submit check

Write the intake as JSON (schema in `references/intake-template.md`) and run
`python3 -I <skill-dir>/scripts/precheck.py <intake.json>`. Fix every FAIL, decide on each WARN,
then walk `references/review-checklist.md` for what a script cannot see.

### Phase 4. Console and channel setup

Follow `references/console-steps.md` and `references/channel-steps.md`. Short order:

0. Create the app if none exists.
1. App basic info (icon, name, 회사명 = registered 상호).
2. Biz app conversion (Owner only, icon needed). No review.
3. 신청 자격 확인.
4. Channel: create it, then business-channel review with the intake documents (human: phone
   verification). Review 3-5 business days.
5. App-channel link request. Review 3-5 business days.
6. 비즈니스 정보 request (auto-approved once linked).
7. Kakao Login ON, redirect URI on the REST API key.
8. Channel public, then 대표 채널 (a private channel cannot be 대표 채널).
9. Terms registered and ON, then 간편가입 ON.
10. 개인정보 동의항목 request with the evidence pack (real services only). Review 3-5 business days.
11. After approval: consent levels and purposes, consent preview.

Test app (only if the user said yes in the intake): `references/console-steps.md` section 6.

### Phase 5. Human moments

Only these need the person: Kakao login and 2FA, account identity verification, the
business-channel review's final attestation checkbox and [동의] plus any 전자증명서 or 대표자 휴대폰 인증
after it, pressing [동의하고 계속하기]
in a real login test, and any approval not given in the intake. Documents themselves were collected
in the intake, so the agent uploads them. For each moment:

1. Call `await task.handOff()` in the current TaskSpace and end the round.
2. Send the filled Korean script from `references/handoffs-ko.md`.
3. After the reply, `takeOverTaskSpace(<id>)` and check the result on screen.

### Phase 6. App code and readback

Read `references/api-readback.md`. The app must key members on Kakao `id`, handle an empty phone
number, read ad consent with `GET /v2/user/service_terms` and store `agreed_at`, read channel
friendship with `GET /v2/api/talk/channels`, and call unlink on withdrawal.

### Phase 7. Report

Report in Korean (an HTML page when over about 60 lines): each step's state with the next action
and owner, review submit dates, masked screenshots, precheck output, and every human moment
with how long it took.

## Reference files

| File | Read it when |
|---|---|
| `references/intake-template.md` | Phase 1: values, files, approvals, test-app question, Korean message, JSON |
| `references/console-steps.md` | Phase 4: menu paths, test-app path, console quirks |
| `references/channel-steps.md` | Creating or linking a Kakao Channel |
| `references/review-checklist.md` | Phase 3: what the reviewer checks |
| `references/rejection-reasons.md` | Before any submit, and after a rejection |
| `references/ad-consent-rules.md` | The service wants marketing messages |
| `references/evidence-pack.md` | The one file the consent-item review needs; masking methods |
| `references/handoffs-ko.md` | Any human moment |
| `references/api-readback.md` | Phase 6, app code |

Scripts: `precheck.py` (pre-submit check), `console-helpers.mjs` (exact-ID scope dialogs, terms,
app-ID guard), `clean-shot.mjs` (masked screenshots), `scan-shots.swift` (OCR leak scan, `--redact`).
The browser helpers are written for ego-browser (`ego-browser nodejs`); adapt the calls for another
browser tool that can use the user's signed-in session.

## Handoff note

For work that spans sessions, keep a note in the user's handoff folder (or the service repo) with
three parts: done, next, and the exact resume command.
