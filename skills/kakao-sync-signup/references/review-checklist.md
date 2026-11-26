# Pre-submit review checklist

Run this before you click 신청 on 개인정보 동의항목 or 카카오톡 채널 연결. Run
`scripts/precheck.py` first; it covers the items marked [script]. Check the rest yourself
in ego-browser and write PASS or FAIL with evidence next to each line in the handoff note.

Main sources:
- Checklist: https://developers.kakao.com/docs/latest/ko/kakaologin/prerequisite#additional-feature-request-checklist
- Review process: https://developers.kakao.com/docs/latest/ko/kakaologin/prerequisite#review-process
- Rejection table: https://developers.kakao.com/docs/latest/ko/kakaologin/faq#reject-reason
- Policy: https://developers.kakao.com/docs/latest/ko/kakaologin/common#policy

What the reviewer compares (review-process): "입력한 신청 정보와 제출한 자료의 일치 여부",
and "현재 서비스의 회원가입 방식 및 개인정보 활용 범위가 신청 내역과 일치하는지 여부".
So every item must say the same thing in four places: the request form, the sign-up
evidence, the privacy policy, and the live service.

## A. App identity

1. [ ] App icon, 앱 이름 and 회사명 match the live service and its business. Mismatch is
   rejection "비즈 앱 정보 수정 필요".
2. [ ] The company name appears on the website (footer) and on every brand channel the
   reviewer may open (app store page, Instagram bio if linked). Missing is rejection
   "스토어/브랜드 표기 누락".
3. [ ] The service is not a hosted shop (Cafe24 and similar). Those set Kakao Sync in the
   host admin, not here ("ECP 앱").
4. [ ] The service is not in a category that 운영 정책 제3조 or 제4조 bars.
4a. [ ] The site footer shows the same company name and business number as the app's
    회사명 and 비즈니스 정보. Kakao checks the footer and rejected a one-digit mismatch
    (DevTalk 149033/3, 145862/4, 133981/2) [script: company name; number if in intake].
4b. [ ] The site is the service's own domain. Blogs, cafes, shared domains and static-only
    hosting (GitHub Pages) are not accepted for business-info review (DevTalk 142570/4,
    145500/4) [script: warns on shared hosting domains].
4c. [ ] Kakao Sync 간편가입 is for businesses only; an individual-developer biz app cannot
    use it (DevTalk 137746/2).

## B. Membership, not a one-off form

5. [ ] The service has real membership: sign-up, log-in, and withdrawal. Kakao refuses to
   review "회원가입 목적이 아닌 이벤트나 상담 등과 같이 일회성 수집을 목적으로 하는 경우".
   An event or webinar registration page alone does not qualify. Frame it as a member
   account that also registers for the event.
6. [ ] The sign-up URL in the form opens a page with the service name and a visible Kakao
   login button [script: reachability]. A link to a page without a login button is
   rejection "로그인 및 가입 경로 불명확".
7. [ ] The site is reachable from outside (no VPN, no basic auth, no IP allowlist)
   [script]. Unreachable is rejection "테스트 앱 사용 안내 / 제출하신 사이트가 접근되지 않습니다".
8. [ ] A withdrawal path exists and calls the unlink API (kakaosync/prerequisite,
   "탈퇴 동선").

## C. Items requested

9. [ ] Request only items the sign-up actually collects. Extra items are rejection
   "수집하지 않는 개인정보".
10. [ ] Do not request CI (`account_ci`) unless the sign-up runs its own identity
    verification (본인인증). A live app was rejected for this
    (seen 2026-11-24): "CI(연계정보)는 자체 회원가입 과정에서 실제 본인인증을 진행하는 서비스에
    한해 검토 후 제공" [script].
11. [ ] 필수 or 선택 for each item is the same in the form, the evidence and the privacy
    policy. Example from Kakao: gender requested 필수 but shown 선택 on the page is a
    rejection ("개인정보 수집 조건 불일치").
12. [ ] Each item's purpose is specific and true. Use the purpose the service really has
    (예: 전화번호: 수강 일정·변경 안내 연락). Kakao's FAQ advises: request 필수 only for
    data the sign-up truly needs; ask for the rest as 선택 or later. Never write 본인인증
    or 본인확인 as a purpose: "단순 카카오 로그인은 본인인증 확인기관에 해당하지 않으므로"
    (App B rejection, see `rejection-reasons.md` section 2) [script: warns].
12a. [ ] Pick the branch from intake item 16 (own sign-up form):
    - **Own form exists** (email/password form, or a step where the service asks for
      fields): request only items that form collects, with the same 필수/선택. Kakao
      reviews "귀사 자체 회원가입 프로세스 기준으로" (App B rejection) and rejects
      items the form does not collect (DevTalk 147924/2, 143849/2). With several sign-up
      types, only items common to all can be 필수 (148112/2).
    - **Kakao-only sign-up**: the privacy policy decides. "일반 회원 가입이 없는 경우,
      개인정보 처리방침에 명확히 기재되어 있을 경우 승인 가능합니다" (DevTalk FAQ 133989/1,
      edited 2026-06-01; also 151729/4). Do not add a post-login form only as evidence:
      Kakao read one as a separate sign-up flow (149858/4), and an extra step did not
      help an item missing from the policy (152776/3). If such a step really exists,
      explain it in the request's 수집 사유.
12b. [ ] Each 필수 field carries a visible 필수 marker in the service's sign-up UI. A
    disabled Next button does not count; reviewers "다양한 필수 입력 UI/UX를 예측하여 심사하지
    않습니다". If the UI has no marker, add a capture of the validation error (DevTalk
    140759/4, 152239/2).
12c. [ ] Field labels name the item exactly. "이름 또는 업체명" was rejected as 이름
    (DevTalk 146710/4). A 주민등록번호 field does not stand for 생일/출생 연도 (141405/4).
12d. [ ] If there are several sign-up types, only items common to all types can be 필수
    (DevTalk 148112/2).
13. [ ] phone_number: the app handles an empty value. Users without KakaoTalk have no
    phone number, and 수집 후 제공 is not available for this item (kakaologin/faq).

## D. Privacy policy

14. [ ] The URL opens without login and returns 200 [script].
15. [ ] It states that the purpose of the data received from Kakao is 회원가입 (member
    sign-up). Missing is rejection "소셜 로그인 수집 목적" [script: keyword].
16. [ ] It lists every requested item [script: keyword per item].
17. [ ] It marks each item 필수 or 선택 [script: keywords present].
18. [ ] It says the data is received through Kakao Login (Kakao Sync policy: the policy
    must reflect "카카오로부터 제공받는 사용자 정보의 처리 내용") [script: keyword].
18a. [ ] Kakao is NOT listed as a processor (처리 위탁 / 수탁자). Kakao Login creates no
    processing contract; staff asked five applicants to remove it (DevTalk 148755/3 and
    others) [script: warns].
18b. [ ] 필수/선택 is attached to each item, not to a section heading. "괄호 안의 '(필수)'가
    무엇을 의미하는지 명확하지 않습니다" (DevTalk 152960/2, 2026-11-23).
18c. [ ] The form's 개인정보 처리방침 field holds the privacy policy URL, not the terms of
    service URL (DevTalk 150043/7) [script].
19. [ ] Retention and destruction on withdrawal are stated. Kakao's policy: on withdrawal
    destroy all personal data, including the member ID (kakaologin/common#policy).
20. [ ] If any data is stored or processed abroad (cloud DB, email or SMS vendor), the
    policy lists the 국외 이전 items and the console 개인정보 국외이전 is filled.
21. [ ] For a social-login-only service, the reviewer judges mainly from the privacy
    policy ("소셜 로그인만 제공하는 서비스의 경우, 개인정보 처리방침을 기준으로 심사합니다").
    Give it extra care.

## E. Evidence file

22. [ ] One file, JPG/JPEG/PNG/PDF, 20 MB or less (see `evidence-pack.md`).
23. [ ] It shows the whole path: 가입 → 로그인 → 탈퇴. Missing steps are rejection
    "회원가입 증빙자료 미비".
24. [ ] The service name is visible in the screens.
25. [ ] Each collected item and its 필수 or 선택 condition is visible.
26. [ ] No personal data anywhere: no real email, phone, name, member ID. Kakao deletes
    the file and rejects at once ("개인정보 마스킹"). The console consent preview shows the
    admin's email: mask it.
27. [ ] If the site is not built yet, a plan or design mock-up is allowed instead of
    screenshots (kakaologin/prerequisite, [C] 회원가입 링크).

## F. Service terms (간편가입)

28. [ ] Every term URL opens and shows the same text that the service uses [script].
29. [ ] Tags match the app code [script: format; you: grep the repo for each tag].
30. [ ] The ad-consent term follows `ad-consent-rules.md` [script].
31. [ ] At least one term is 필수 and ON before 간편가입 ON.

## G. Channel link (if requested)

32. [ ] The channel is a 비즈니스 채널, not linked to another app, and its business
    number equals the app's. Otherwise it does not appear in the list.
33. [ ] You hold 마스터 or 매니저 on the channel and Owner or Editor on the app.

## H. After submit

34. [ ] Record the submit date. Expect 3-5 business days.
35. [ ] On rejection, read the reason under 앱 > 추가 기능 신청 > 심사 사유 > 확인, match
    it in `rejection-reasons.md`, fix, and re-apply from the same 신청 button. In the
    re-application, write what you fixed and where (수집 사유 or 추가 정보 field), as the
    DevTalk FAQ asks (133989/1).
36. [ ] For questions, Kakao wants a DevTalk private message, not a public post, with the
    company name, the app ID and whether a hosting company is used.
