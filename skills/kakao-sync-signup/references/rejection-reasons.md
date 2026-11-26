# Known rejection reasons

Read before any submit, and after a rejection. Match the rejection message in the
console (앱 > 추가 기능 신청 > 심사 사유 > 확인) to a row, apply the fix, re-apply from the
same 신청 button. Re-review takes another 3-5 business days, so prevention is cheaper.

## Contents

1. Official rejection table (개인정보 동의항목)
2. Observed in real apps (anonymized)
3. Business channel review (Kakao Business)
4. Service terms and 간편가입
5. DevTalk threads (table, fixes, rule change, gaps)

## 1. Official rejection table

Source: https://developers.kakao.com/docs/latest/ko/kakaologin/faq#reject-reason
(read in full 2026-11-24). Quotes are the console messages.

| Message (console) | Cause | Fix |
|---|---|---|
| 수집하지 않는 개인정보: "회원가입 시 수집하는 항목과 심사 신청 항목이 일치하지 않습니다." | Requested an item the sign-up does not collect | Remove it, or add it to the sign-up page first |
| 화면 오등록: "회원가입 시 수집하는 개인정보를 확인할 수 있는 화면으로 첨부해 주세요." | Evidence does not show the collected items | Rebuild the evidence pack, screen 2 |
| 비즈 앱 정보 수정 필요: "비즈 앱 정보(앱 아이콘, 이름, 회사명)이 서비스 정보와 일치하지 않습니다." | App icon, name or company differs from the service | Fix 앱 > 일반 > 기본 정보 |
| 개인정보 마스킹: "제출하신 회원가입 화면 내 개인정보가 포함되어 있습니다." | Unmasked personal data in evidence. Kakao deletes the file at once | Mask everything, including the admin email in the consent preview |
| 회원가입 증빙자료 미비: "첨부하신 자료로는 회원가입 절차를 확인할 수 없습니다." | Evidence lacks part of 가입 → 로그인 → 탈퇴 | Add the missing screens; show items and 필수/선택 |
| 개인정보 수집 조건 불일치 | 필수/선택 differs between request and sign-up page | Make them equal everywhere |
| 개인정보 수집 조건 미표기: "회원가입 화면 내 항목의 필수 수집 조건을 확인할 수 없습니다." | Sign-up page or policy lacks 필수/선택 marks | Mark each item on the page and in the policy |
| 소셜 로그인 개인정보 처리방침: "개인정보 처리방침 링크를 확인해 주세요." | Policy URL broken, or it lacks purpose, items, conditions | Fix the page; run `precheck.py` |
| 소셜 로그인 수집 목적: "개인정보 처리방침 내 개인정보 수집 목적이 심사 기준에 맞지 않습니다." | Policy does not say the purpose is 회원가입 | Write "회원가입" as the purpose, list the real items |
| ECP 앱 | Service uses a hosting company's Kakao Sync | Configure in the host admin |
| 테스트 앱 사용 안내: "제출하신 사이트가 접근되지 않습니다." | Site not reachable | Make it public, or upload screens of the flow |
| 심사 대기 30일 경과 | Business-info review pending 30+ days | Finish business info first, then re-apply |
| 삭제된 앱 | App deleted | Use a new or other app |
| 스토어/브랜드 표기 누락 | No company name on the site, store page or brand channels | Show the company name; reviewers check external channels too |
| 로그인 및 가입 경로 불명확 | Submitted link differs from the real flow, or no login button | Upload a file that explains 가입, 로그인, 탈퇴 |
| 운영 정책 위반 | Service barred by 운영 정책 제3조/제4조 | Not reviewable |
| One-off collection | "회원가입 목적이 아닌 이벤트나 상담 등과 같이 일회성 수집을 목적으로 하는 경우" | Not reviewable. Needs real membership |

Kakao also states (kakaologin/prerequisite): "카카오 로그인과 같이 소셜 로그인만 제공하는
서비스의 경우, 개인정보 처리방침을 기준으로 심사합니다."

For questions about a rejection, Kakao asks for a DevTalk private message (not a public
post) with: the company name on the business registration, the biz app ID, and whether a
hosting company is used.

## 2. Observed in real apps (anonymized)

### App A (education service): CI request rejected

Seen in the console on 2026-11-24 (앱 > 추가 기능 신청 > 개인정보 동의항목 > 확인):

- Request: 필수 항목: CI(연계정보)
- Reason (verbatim): "서비스에서 수집하지 않는 CI(연계정보) 항목은 신청할 수 없습니다.
  CI(연계정보)는 자체 회원가입 과정에서 실제 본인인증을 진행하는 서비스에 한해 검토 후
  제공하고 있으며, 회원 비교 식별 목적으로만 활용 가능합니다. 회원가입 화면 또는
  개인정보처리방침으로는 신청할 수 없습니다."
- Lesson: request CI only if the sign-up runs its own identity verification (PASS,
  phone carrier check) and only to match existing members. `precheck.py` fails a CI
  request unless the intake sets `own_identity_verification: true`.
- The earlier grants still stand: name, email and phone are set to 필수 on the same app.

### App B (sports community): request did not match the service's own sign-up form

Seen in the console on 2026-11-24 (read-only):

- Request: 필수 항목: 이름, 생일, 출생 연도, 카카오계정(전화번호); 선택 항목: 성별
- Reason (verbatim): "회원가입 시 수집하는 항목과 심사 신청 항목이 일치하지 않습니다.
  회원가입 시 수집하지 않는 항목( 이름, 생일, 출생 연도, 전화번호, 성별 )은 제외 후 신청해
  주세요. → 개인정보 동의항목은 소셜 로그인 기능이 아닌 귀사 자체 회원가입 프로세스 기준으로
  심사 진행되는 점 참고 바랍니다. → 단순 카카오 로그인은 본인인증 확인기관에 해당하지
  않으므로 본인인증이 필요하신 경우 서비스 자체에서 본인인증이 진행되어야 합니다."
- Context from the service's own docs: App B has its own sign-up form (이름·생년월일 필수) and collects the
  phone number by a separate phone check after sign-up. Its privacy policy then in force
  (v0.2) said 전화번호 필수 at sign-up, which the repo notes did not match the screen.
- Lessons:
  1. With an own sign-up form, the request must match that form item by item and
     필수/선택 by 필수/선택. Gender was requested but not collected; phone was requested as
     필수 but not collected in the form. Fix the request, not the evidence.
  2. Do not give 본인인증 or 본인확인 as a purpose. Kakao Login is not an identity
     verification provider. Use the real business purpose (예: 수업 안내 연락, 연령별 코스
     추천). `precheck.py` warns on such purposes.
  3. Request only what the product uses now. Birthday and birth year together, both
     필수, invite the question "why both".

## 3. Business channel review

Source: https://kakaobusiness.gitbook.io/main/channel/start (2-2, 2-5).

- Document does not match the business registration number.
- Personal data not masked.
- Low resolution or cut-off image.
- Channel name differs from the company name with no explanation in 사업자정보 불일치 소명.
- Missing business license for licensed industries (food, medical, lodging, education
  services, alcohol, tobacco, adult games).
- Pre-launch service. Rejection text received 2026-11-26 for a service whose site said
  "출시 전": "[전환 불가-정식 사업 미개시] 정식 사업 시작 후 신청 가능 (CBT, OBT, 사이트 미완성 시
  전환 불가)". Cause: the service was not open to the public. Fix: none until launch. Gate this
  with intake C9 before Step 2.
- After a rejection, reapply from 채널 관리자센터 (PC) > 관리 > 비즈니스 채널 신청 > [재신청], or in
  the app 채널 관리 > 비즈니스 채널 > 심사 반려. "심사 반려 30일 이후 또는 심사 포기 후에는 기존에
  제출하신 모든 서류가 파기됩니다. 재신청 시 필수 서류를 재첨부 해주세요." (Kakao reapply guide image
  linked from the rejection mail, https://kko.kakao.com/PQQvMs_goj)

## 4. Service terms and 간편가입

There is no review for terms, but Kakao warns on the 간편가입 page (seen 2026-11-24) that a
false app registration, or terms that do not fit the service or ignore laws and
government guides, can restrict the service. Source for "the registered term must equal
the real term": https://developers.kakao.com/docs/latest/ko/kakaologin/common#policy-terms

The KISA guide makes an ad-consent title such as "마케팅 동의" or "혜택 알림 동의" invalid
as consent. See `ad-consent-rules.md`.

## 5. DevTalk threads

Threads from https://devtalk.kakao.com where Kakao staff explained a rejection. Each row
has the thread URL and the staff answer's date.

Collected 2026-11-24 from 58 threads through the Discourse JSON API. All 67 rows were
re-checked the same day by a separate script over `/posts/by_number/<topic>/<post>.json`:
the quote is in the post text, the post has the staff, moderator or admin flag, and the
date matches. Type: 1 = 개인정보 동의항목, 2 = 비즈니스 정보 /
비즈 앱 / 채널 연결, 3 = 간편가입 terms. Staff accounts: tim.l, woody.ho, kakao (FAQ).

| type | rejection reason or rule | verbatim quote (Kakao staff post) | thread URL | post date |
|---|---|---|---|---|
| 1 | FAQ: wrong evidence (privacy-policy or home screen instead of the signup input screen) [blockquote] | 회원가입 페이지의 개인정보 입력 화면을 제출해야하나 개인정보처리방침 화면, 홈 화면 등으로 잘못 등록하는 경우 | https://devtalk.kakao.com/t/faq/132333/1 | 2023-10-17 (FAQ, last edited 2025-12-09) |
| 1 | FAQ: required/optional condition in request differs from the signup form [blockquote] | 회원가입 시 필수, 선택으로 수집하는 항목의 조건과 심사 요청한 필수, 선택 항목의 조건이 불일치 | https://devtalk.kakao.com/t/faq/132333/1 | 2023-10-17 (FAQ, last edited 2025-12-09) |
| 1 | Requested items are not collected in the signup form (email/name only) | 회원님 서비스의 일반회원가입에서는 이메일, 이름만을 취급하고 있어 신청하신 항목은 모두 반려되었습니다. | https://devtalk.kakao.com/t/topic/147924/2 | 2026-01-12 |
| 1 | Applied [required] but the signup form collects the items as optional | 운영하시는 서비스의 회원가입 시, 이름/생일/전화번호가 필수 입력이 아닙니다. | https://devtalk.kakao.com/t/topic/143849/2 | 2025-04-22 |
| 1 | Required status shown only by a disabled Next button is not accepted; mark it in the UI | 우측 상단 버튼의 비활성으로 사용자가 특정 필드 값이 필수 입력을 요구하는 것을 쉽게 인지할 수 있다고 볼수 없을 것 같습니다. | https://devtalk.kakao.com/t/topic/140759/4 | 2024-11-19 |
| 1 | Reviewers do not infer required fields; show the validation (error) screen | 심사팀에서는 서비스측의 다양한 필수 입력 UI/UX를 예측하여 심사하지 않습니다. | https://devtalk.kakao.com/t/topic/152239/2 | 2026-10-19 |
| 1 | Field label differs from the item ("이름 또는 업체명") and was optional | 회원가입 회면을 보니 "이름 또는 업체명"으로 이름을 선택적으로 입력하도록 되어 있어 반려된 것으로 보입니다. | https://devtalk.kakao.com/t/topic/146710/4 | 2025-10-16 |
| 1 | Several signup types: only items common to all types can be [required] (reviewer wording relayed) | 공통적으로 필수 수집하는 항목만 필수 수집 신청 가능합니다. | https://devtalk.kakao.com/t/topic/148112/2 | 2026-01-23 |
| 1 | Kakao Login is only for signup, not for plain data collection | 카카오 로그인은 서비스의 회원가입 목적으로만 제공되며 단순 개인정보 수집목적으로는 제공하지 않는점 양해 부탁드립니다. | https://devtalk.kakao.com/t/topic/147620/3 | 2025-12-18 |
| 1 | Event-entry data collection is rejected | 신청하신 내용은 이벤트용 개인정보 취득이라 반려된 것으로 확인됩니다. | https://devtalk.kakao.com/t/topic/146451/10 | 2025-09-24 |
| 1 | Signup on a sub-page (promotion or consultation) instead of the main service | 공식 회원가입이 아닌 단순히 개인정보 취득 편의용으로 카카오 로그인 사용 시, 추가 개인정보 동의항목은 설정 권한 제공하고 있지 않습니다. | https://devtalk.kakao.com/t/topic/144429/2 | 2025-05-28 |
| 1 | Button text did not read as signup ("지금 바로 투표하기") | 심사팀에서는 회원가입 이용자 동선과 표기상 “지금 바로 투표하기” 버튼을 보고이용자가 회원가입으로 인식하기 어렵다고 판단한 것 같습니다. | https://devtalk.kakao.com/t/topic/144216/2 | 2025-05-16 |
| 1 | Input field on an unrelated page (my page, marketing phone) does not qualify | 이용자 가입 동선과 무관한 페이지에 입력 기능을 두어 개인정보 취득 편의용으로는 심사가 어려운점 양해 부탁드립니다. | https://devtalk.kakao.com/t/topic/148848/10 | 2026-03-23 |
| 1 | Privacy policy must state signup purpose, withdrawal, rights and retention | 카카오디벨로퍼스 이용약관상 서비스는 탈퇴 기능을 반드시 제공해야 함으로 해당 기능의 제공과 함께 이와 관련된 권리 행사 방법과 보유 및 이용 기간 내용을 개인정보처리방침 내 포함 하셔야 합니다. | https://devtalk.kakao.com/t/topic/149414/2 | 2026-04-23 |
| 1 | Privacy policy lists items without 필수/선택 (reviewer wording relayed) | 개인정보처리방침 내 ( 이름, 성별, 연령대, 전화번호 ) 항목은 수집 조건(필수/선택)이 확인되지 않습니다. 수집 조건을 추가해 주세요. | https://devtalk.kakao.com/t/topic/152701/2 | 2026-11-10 |
| 1 | Ambiguous "(필수)" on a section heading is not accepted | 괄호 안의 ‘(필수)’가 무엇을 의미하는지 명확하지 않습니다. | https://devtalk.kakao.com/t/topic/152960/2 | 2026-11-23 |
| 1 | Requested item (배송지) is not in the privacy policy; an extra post-login step does not help | 현재 반려사유는 개인정보 처리방침 내 기재되어 있지 않은 항목에 대해 심사 요청하여 반려된 것입니다. | https://devtalk.kakao.com/t/id-1605786/152776/3 | 2026-11-13 |
| 1 | Privacy policy lists Kakao as a processor (위탁); remove it | 만약, 카카오 로그인 이용에 의해 표시하신 거라면 성립되지 않는 관계이기에 제거 부탁드리며 알림톡/상담톡 이용에 의한 표기라면 알림톡 딜러사를 표기하셔야 합니다. | https://devtalk.kakao.com/t/topic/148755/3 | 2026-03-12 |
| 1 | Terms-of-service URL submitted in the privacy-policy field | 앞서 첨부해주신 URL은 개인정보 처리방침이 아닌 서비스 이용약관으로 회원님 서비스의 개인정보 처리방침 URL을 첨부 부탁드립니다. | https://devtalk.kakao.com/t/topic/150043/7 | 2026-06-04 |
| 1 | Kakao-only signup is judged by the privacy policy; with a signup form, items must match it | 카카오로그인만 있는 경우, 개인정보 처리 방침에 따라 제공됩니다. | https://devtalk.kakao.com/t/topic/151729/4 | 2026-09-21 |
| 1 | Post-Kakao-login form was read as a separate signup flow; explain it in the request | 심사팀에서는 해당 동선은 카카오 로그인과 별개의 회원가입 동선으로 본 것 같습니다. | https://devtalk.kakao.com/t/topic/149858/4 | 2026-05-21 |
| 1 | Signup flow did not work for the reviewer (returned to login screen) | 일반회원가입 과정을 직접 확인하고자 하여도 다시 로그인 화면으로 돌아오는 등의 이유로 반려된 것으로 보이는점 참고 부탁드립니다. | https://devtalk.kakao.com/t/topic/149001/2 | 2026-03-30 |
| 1 | Signup link was a demo page, not a real flow | 제출하신 회원가입링크의 경우 데모페이지로 실제 이용되지 않는 회원가입 절차인점 확인되어 반려되었습니다. | https://devtalk.kakao.com/t/kakao-sync/149946/2 | 2026-05-27 |
| 1 | Screens of another business were submitted | 아쉽지만, 타 사업자 화면을 기준으로 심사 할 수 없습니다. | https://devtalk.kakao.com/t/topic/140739/4 | 2024-11-18 |
| 1 | Collecting 주민등록번호 does not stand in for 생일/출생 연도 | 주민등록번호 수집동의가 생일, 출생년도 동의를 의미하지 않습니다. | https://devtalk.kakao.com/t/topic/141405/4 | 2024-12-19 |
| 1 | CI requires identity verification by a certified agency (본인확인기관) | (1) 본인 확인 기관에 의한 본인 인증이 없으므로 CI는 승인 받을 수 없습니다. | https://devtalk.kakao.com/t/topic/151376/3 | 2026-08-27 |
| 1 | CI: KG이니시스 simple authentication is not 본인확인 (corrects earlier replies in the thread) | KG 이니시스통한 인증은 본인확인 기관에의한 본인 인증이 아니라 카카오로그인의 CI와 마찬가지로 운영하시는 서비스에서 CI 수집 불가한 것으로 확인하였습니다. | https://devtalk.kakao.com/t/ci/148813/21 | 2026-03-17 |
| 1 | Cafe24 shops must not apply; settings sync from Cafe24 | 카페24를 사용하시는 경우 심사 요건에 맞게 시스템 적용되므로 별도 심사 신청 하실 필요 없고 카페24에서 카카오로그인 설정 및 개인정보 동의항목 설정하시면 동기화됩니다. | https://devtalk.kakao.com/t/topic/150370/4 | 2026-06-25 |
| 1 | Unmasked personal data in an attachment means rejection regardless of content | (개인정보가 있는 경우 내용 무관 반려 처리되고, 첨부파일은 즉시 파기됩니다.) | https://devtalk.kakao.com/t/ci/148813/5 | 2026-03-16 |
| 1 | FAQ (current text): Kakao-only signup is approved when the privacy policy states the items | 일반 회원 가입이 없는 경우, 개인정보 처리방침에 명확히 기재되어 있을 경우 승인 가능합니다. | https://devtalk.kakao.com/t/faq/133989/1 | 2023-12-22 (FAQ, last edited 2026-06-01) |
| 1 | FAQ: write the fix and its location in the request (수집 사유 / 추가 정보) [blockquote] | 원활한 심사를 위해 반려 사유에 대한 조치 내역은 가급적 심사 신청 시, 조치 위치 및 내용을 기재 부탁드립니다. | https://devtalk.kakao.com/t/faq/133989/1 | 2023-12-22 (FAQ, last edited 2026-06-01) |
| 2 | Business name on the registration certificate must appear in the service and in the app's company name | 1)사업자등록증에 표기된 상호명이 회원님 서비스 내에도 표시되어 있어야 하며, 2) 앱의 회사명에도 동일하게 등록되어 있어야만 합니다. | https://devtalk.kakao.com/t/topic/145862/4 | 2025-08-21 |
| 2 | Match the certificate name to the app's 회사명, not to the app name | 비즈앱 이름과 사업자등록증상의 상호명을 일치시키는 것이 아닌 사업자등록증 상호와 디벨로퍼스앱 회사명 일치입니다. | https://devtalk.kakao.com/t/topic/147923/4 | 2026-01-14 |
| 2 | Business number in the site footer differs from the app (one digit) | https://in-farm.co.kr/ 사이트 Footer의 사업자번호는 374-81-00172 이고 디벨로퍼스앱에 등록된 사업자번호는 374-81-00142 입니다. | https://devtalk.kakao.com/t/topic/149033/3 | 2026-04-01 |
| 2 | Footer business info is checked to match the app | 운영하시는 서비스와 디벨로퍼스앱간 일치 확인을 위해 Footer 정보를 확인합니다. | https://devtalk.kakao.com/t/topic/133981/2 | 2023-12-22 |
| 2 | Footer shows two businesses without distinction | 사이트에는 두개의 사업자가 구분 없이 표기 되어 있어서 그런것 같습니다. | https://devtalk.kakao.com/t/topic/145381/2 | 2025-07-28 |
| 2 | FAQ: a development agency must register the site owner's business | 디벨로퍼스앱의 정보는 카카오 로그인을 비롯한 다양한 연관 서비스에 노출되므로 사이트의 소유자와 동일한 사업자로 대행 등록해주셔야합니다. | https://devtalk.kakao.com/t/faq/133989/1 | 2023-12-22 (FAQ, last edited 2026-06-01) |
| 2 | Blogs, cafes and shared domains (e.g. Google Sites) are not accepted | 각종 블로그, 카페, 공용도메인 등으로 비즈니스 정보심사는 진행할 수 없는 부분 양해 부탁드립니다. | https://devtalk.kakao.com/t/topic/142570/4 | 2025-02-17 |
| 2 | Static-only sites (GitHub Pages) are not accepted | github pages와 같은 정적 서비스로만 제공되는 경우도 비즈니스 정보 심사 상 허용하고 있지 않은점 양해 부탁드립니다. | https://devtalk.kakao.com/t/topic/145500/4 | 2025-08-04 |
| 2 | Site not finished [blockquote] | 사이트가 덜 구축된 것으로 보입니다. 구축 완료 후, 심사 신청해주세요. | https://devtalk.kakao.com/t/topic/134912/2 | 2024-02-05 |
| 2 | No withdrawal menu or data deletion | 카카오로그인으로 개인정보 항목을 동의 받아 처리한 경우 탈퇴 메뉴를 제공하고 개인정보 파기 절차를 제공하셔야합니다. | https://devtalk.kakao.com/t/topic/150933/4 | 2026-07-31 |
| 2 | Low-resolution service screenshots (reviewer wording relayed) | 서비스화면 이미지 해상도가 낮아 정상적인 확인이 어렵습니다. | https://devtalk.kakao.com/t/topic/145312/2 | 2025-07-24 |
| 2 | Personal data (a phone number) in the submitted PDF | 심사 시, 제출된 내용 중 개인정보가 포함된 경우 이를 즉시 파기하기위해 승인 가능 여부과 상관없이 반려하고 있는점 참고 부탁드립니다. | https://devtalk.kakao.com/t/topic/149134/2 | 2026-04-07 |
| 2 | Content behind login: attach screens of the whole service | 심사 신청 시, 심사팀에서 이러한 내용의 확인이 가능할 수 있도록 서비스 전반에 대한 내용을 “서비스 화면” 항목에 첨부 부탁드립니다. | https://devtalk.kakao.com/t/topic/148686/2 | 2026-03-09 |
| 2 | Site blocked from Kakao's internal network; attach captures | 카카오 사내 망에서 접근할 수 없도록 차단된 사이트로 확인됩니다. | https://devtalk.kakao.com/t/topic/139449/2 | 2024-09-03 |
| 2 | Matchmaking services need adult verification (운영정책) | 디벨로퍼스 운영정책에 따라 미성년자 보호를 위해 만남주선 등의 서비스는 서비스내 성인인증 기능이 있어야합니다. | https://devtalk.kakao.com/t/topic/145893/2 | 2025-08-25 |
| 2 | Adult-only service: verify age at signup, including the Kakao Login path | 회원님 서비스가 성인만 이용할 수 있는 서비스인 경우 제품 구매 시점에 성인인증을 요구할 것이 아닌 회원 가입 과정부터 제한하도록 부탁드립니다. | https://devtalk.kakao.com/t/topic/147491/4 | 2025-12-09 |
| 2 | Lending services need the required license or registration | 국내 법에 따른 대부업신고 또는 전자금융업 등록 등. 사업유형에 따른 필요한 허가·등록을 하셔야 권한 승인됩니다. | https://devtalk.kakao.com/t/topic/145197/4 | 2025-07-17 |
| 2 | Reselling usage rights without a contract with the provider | 서비스 제공사와 직접 제휴/계약하지 않고 사용권을 재판매하는 경우 아래 운영정책에 따라 카카오디벨로퍼스 서비스를 사용하실 수 없습니다. | https://devtalk.kakao.com/t/id/151163/2 | 2026-08-14 |
| 2 | Channel in the service screens differs from the channel link given | 제공하신 서비스 화면에 표시된 채널과 추가 정보로 제공하신 채널은 서로 다른 채널입니다. | https://devtalk.kakao.com/t/topic/150040/4 | 2026-06-04 |
| 2 | Link the app to the real business channel first; then the channel review result is reused | 이 경우 비즈니스채널 심사 결과를 준용하여 바로 승인 절차가 진행됩니다. | https://devtalk.kakao.com/t/topic/150040/6 | 2026-06-04 |
| 2 | App and channel registered to different businesses cannot be linked | 다른 사업자간의 앱-채널 연결은 지원하지 않고 있는데요. | https://devtalk.kakao.com/t/topic/148458/10 | 2026-02-20 |
| 2 | Operating channel linked to the test app blocks linking it to the live app | 테스트앱에서 운영채널은 연결 해제 해주세요. | https://devtalk.kakao.com/t/topic/142570/18 | 2025-02-17 |
| 2 | Kakao Sync 간편가입 is for businesses only, not individual-developer biz apps | 카카오싱크(개인정보 동의항목 심사) 신청에 의한 간편가입의 경우 사업자만 사용 가능합니다. | https://devtalk.kakao.com/t/topic/137746/2 | 2024-06-17 |
| 3 | At least one required term; optional-only terms are not allowed | 서비스 약관은 선택 약관 만으로 설정할 수 없으며 반드시 1개 이상 필수 동의 약관이 포함되어 있어야만 합니다. | https://devtalk.kakao.com/t/topic/144390/4 | 2025-05-26 |
| 3 | Kakao lets you set a marketing term as optional; its legality is your responsibility | 카카오는 마케팅 동의 항목을 “선택” 동의 항목으로 설정할 수 있도록 기능적 지원을 하고 있지만, 내용이 적법 한지는 서비스에서 주의 깊게 판단하셔야 합니다. | https://devtalk.kakao.com/t/topic/144390/4 | 2025-05-26 |
| 3 | Sync terms should be the same terms as the normal signup | 일반적으로 카카오싱크 간편가입에 포함되는 약관은 서비스의 실제 회원가입 과정에서 이용자가 동의해야 하는 약관과 동일해야 하며 | https://devtalk.kakao.com/t/topic/148707/8 | 2026-03-10 |
| 3 | No nested or grouped terms | 간편가입의 약관은 개별적인 동의 단위로 명확히 인지할 수 있도록 설계되어 있어, 계층 구조나 그룹 단위는 지원하고 있지 않으며 관련한 지원 계획은 없습니다. | https://devtalk.kakao.com/t/topic/151765/2 | 2026-09-18 |
| 3 | Each term needs a unique tag; one URL can back two terms | 태그 값은 서비스 약관을 구분하기 위해 사용되며 동일한 값을 사용할 수 없습니다. | https://devtalk.kakao.com/t/url/135523/2 | 2024-03-05 |
| 3 | One URL for several terms is acceptable if each title's content is reachable | 각각의 제목에 따른 내용을 해당 링크에 진입하여 확인만 할 수 있으면 됩니다. | https://devtalk.kakao.com/t/topic/127382/2 | 2023-01-26 |
| 3 | The channel-relationship scope (plusfriends) is not ad consent | 광고성 정보에 대한 수신을 고객이 동의한 것으로 볼 수 없습니다. | https://devtalk.kakao.com/t/topic/134210/4 | 2024-01-05 |
| 3 | Channel add (ad consent) cannot be made required | 네, 동의 자체는 광고 동의이므로 법적으로 불가합니다. | https://devtalk.kakao.com/t/topic/148458/14 | 2026-02-24 |
| 3 | Brand messages need the service's own consent | 브랜드 메시지 사용하는 경우 반드시 이용자 동의를 받아야합니다. | https://devtalk.kakao.com/t/topic/151064/4 | 2026-08-12 |
| 3 | Marketing-purpose collection needs a separate optional consent | 이와 별개로 마케팅 목적의 개인정보 수집은 이용자로부터 별도 [선택] 동의를 받으셔야합니다. | https://devtalk.kakao.com/t/topic/148848/7 | 2026-03-23 |
| 3 | The built-in 14-year age term is not adult verification | 해당 항목은 14세 미만 법정대리인 동의 과정을 지원하기 제공되는 기능으로 성인인증을 위한 기능이 아닌데요 | https://devtalk.kakao.com/t/topic/148948/2 | 2026-03-26 |
| 3 | 간편가입 needs app-channel link and business review first | 앱-채널 연결 및 비즈니스 정보심사 승인 후, 간편가입 설정 에서 서비스 약관 활성화 하시면됩니다. | https://devtalk.kakao.com/t/topic/151240/4 | 2026-08-28 |
| 3 | Adding only optional terms does not re-show the consent screen [blockquote] | 선택약관만이 추가되었다면 동의 화면이 출력되지 않습니다. | https://devtalk.kakao.com/t/topic/130624/2 | 2023-07-14 |

### Fixes applicants had to make (3+ threads each)

1. Make each requested item and its 필수/선택 condition match the own signup form, or apply for [선택] instead. https://devtalk.kakao.com/t/topic/143849/2 , https://devtalk.kakao.com/t/topic/147924/2 , https://devtalk.kakao.com/t/topic/151214/2 , https://devtalk.kakao.com/t/topic/146710/4 , https://devtalk.kakao.com/t/topic/147517/2 , https://devtalk.kakao.com/t/topic/151376/3
2. Show the required status explicitly: a 필수 marker per field, or a capture of the validation/error screen. https://devtalk.kakao.com/t/topic/140759/4 , https://devtalk.kakao.com/t/topic/148914/2 , https://devtalk.kakao.com/t/topic/152239/2 , https://devtalk.kakao.com/t/topic/145910/4 , https://devtalk.kakao.com/t/topic/146710/4
3. Rewrite the privacy policy: list every requested item with an explicit 필수/선택 and the signup purpose. https://devtalk.kakao.com/t/topic/152701/2 , https://devtalk.kakao.com/t/topic/152960/2 , https://devtalk.kakao.com/t/topic/145901/2 , https://devtalk.kakao.com/t/topic/145542/2 , https://devtalk.kakao.com/t/topic/149414/2
4. Delete Kakao from the 위탁 (processor) table in the privacy policy. https://devtalk.kakao.com/t/topic/148755/3 , https://devtalk.kakao.com/t/topic/147831/4 , https://devtalk.kakao.com/t/topic/151757/2 , https://devtalk.kakao.com/t/topic/149611/5 , https://devtalk.kakao.com/t/id-1598089/152914/2
5. Put the privacy-policy URL in the privacy-policy field, not the terms-of-service URL. https://devtalk.kakao.com/t/topic/150043/7 , https://devtalk.kakao.com/t/topic/145910/4 , https://devtalk.kakao.com/t/topic/150040/9
6. Reframe the use as signup (with a member DB and withdrawal), not event entry, consultation or data lookup. https://devtalk.kakao.com/t/topic/147620/3 , https://devtalk.kakao.com/t/topic/146451/10 , https://devtalk.kakao.com/t/topic/148458/4 , https://devtalk.kakao.com/t/topic/144429/2 , https://devtalk.kakao.com/t/topic/152262/2 , https://devtalk.kakao.com/t/topic/137143/4
7. Give a signup entry URL that works for an outside reviewer, on the applicant's own live site (no demo page, no other business's screens). https://devtalk.kakao.com/t/topic/149001/2 , https://devtalk.kakao.com/t/topic/137562/4 , https://devtalk.kakao.com/t/topic/149532/3 , https://devtalk.kakao.com/t/kakao-sync/149946/2 , https://devtalk.kakao.com/t/topic/140739/4
8. Add a withdrawal (탈퇴) menu that deletes personal data, and show it in the submission. https://devtalk.kakao.com/t/topic/150933/4 , https://devtalk.kakao.com/t/topic/145500/4 , https://devtalk.kakao.com/t/topic/140739/2 , https://devtalk.kakao.com/t/topic/146451/12 , https://devtalk.kakao.com/t/topic/150043/7
9. Make business name and number identical on the 사업자등록증, the app's 회사명 / business info, and the site footer. https://devtalk.kakao.com/t/topic/145862/4 , https://devtalk.kakao.com/t/topic/147923/4 , https://devtalk.kakao.com/t/topic/149033/3 , https://devtalk.kakao.com/t/topic/145299/2 , https://devtalk.kakao.com/t/topic/145312/2 , https://devtalk.kakao.com/t/topic/142570/4
10. Mask all personal data (phone, email, IDs, test accounts) in attachments, then resubmit. https://devtalk.kakao.com/t/ci/148813/5 , https://devtalk.kakao.com/t/topic/149134/2 , https://devtalk.kakao.com/t/topic/151634/2 , https://devtalk.kakao.com/t/topic/145299/4 , https://devtalk.kakao.com/t/topic/134884/2
11. Add adult or identity verification at signup (also on the Kakao Login path) for matchmaking or adult services. https://devtalk.kakao.com/t/topic/145893/2 , https://devtalk.kakao.com/t/topic/147491/4 , https://devtalk.kakao.com/t/topic/144798/2 , https://devtalk.kakao.com/t/topic/149287/3 , https://devtalk.kakao.com/t/topic/145106/5 , https://devtalk.kakao.com/t/topic/151634/2
12. For CI: add identity verification by a certified agency (본인확인기관) to the Kakao signup path, or drop CI. https://devtalk.kakao.com/t/topic/146222/2 , https://devtalk.kakao.com/t/ci/148813/21 , https://devtalk.kakao.com/t/topic/151376/3 , https://devtalk.kakao.com/t/topic/135515/2 , https://devtalk.kakao.com/t/topic/137918/2
13. In the resubmission, write what was fixed and where (수집 사유 or 추가 정보) and paste the DevTalk thread URL. https://devtalk.kakao.com/t/faq/133989/1 , https://devtalk.kakao.com/t/topic/149126/6 , https://devtalk.kakao.com/t/topic/145608/6 , https://devtalk.kakao.com/t/topic/139449/2 , https://devtalk.kakao.com/t/api/143415/4 , https://devtalk.kakao.com/t/topic/144798/4 , https://devtalk.kakao.com/t/topic/137606/4



### Rule change to flag

- 2024 staff answers limited Kakao-only signup (no own signup form) to 이름 and 전화번호. Example, quoting the FAQ text of that time: "이름과 전화번호’항목에 한해서만 개인정보 처리방침에 명확히 기재되어 있을 경우 승인 가능합니다." https://devtalk.kakao.com/t/topic/138564/2 (2024-07-24). Same limit: https://devtalk.kakao.com/t/topic/137143/4 , https://devtalk.kakao.com/t/topic/138687/2 , https://devtalk.kakao.com/t/topic/137274/2
- The current FAQ text (version 15; last edited 2026-06-01; the edit that removed the limit is not known) has no item limit: "일반 회원 가입이 없는 경우, 개인정보 처리방침에 명확히 기재되어 있을 경우 승인 가능합니다." https://devtalk.kakao.com/t/faq/133989/1 . 2026 answers apply the privacy-policy rule to other items (성별 in https://devtalk.kakao.com/t/topic/150043/7 , 생일/출생 연도 in https://devtalk.kakao.com/t/topic/151729/4 ). Treat the 2024 name/phone limit as superseded.
- CI thread 148813: posts #5 and #14 said KG이니시스 could give optional CI consent; post #21 retracts this. The CI row cites #21. Post #5 is cited only for its masking sentence.

### Gaps (type 3)

- No thread found where a 간편가입 service-term registration itself was rejected. Type 3 rows are staff rules, not rejection reasons.
- No staff quote found on how a 광고성/마케팅 term title must be worded. Staff only say legality is the service's call (https://devtalk.kakao.com/t/topic/144390/4).
- Staff point to Kakao's own "서비스 약관 운용 가이드" for terms rules: https://developers.kakao.com/docs/latest/ko/kakaologin/common#policy-terms (link taken from https://devtalk.kakao.com/t/topic/148707/8 ; page not read in this task).

- The ad-term title rule in this skill comes from the KISA guide, not from DevTalk. See
  `ad-consent-rules.md`.
- The consent-screen channel line is an ad consent. Staff (tim.l, 2024-01-05,
  https://devtalk.kakao.com/t/topic/134210/4): with a 대표 채널 the screen shows
  "[선택] {앱이름}의 광고와 마케팅 메시지를 카카오톡으로 받습니다."; the `plusfriends` scope
  itself only allows reading the relationship and "광고성 정보에 대한 수신을 고객이 동의한 것으로
  볼 수 없습니다". So channel-add covers channel messages only. SMS, email and other
  KakaoTalk ad sends still need the 광고성 정보 수신 동의 term.
