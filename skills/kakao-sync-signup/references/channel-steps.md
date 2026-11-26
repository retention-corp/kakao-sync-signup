# Kakao Channel (카카오톡 채널) steps

Kakao Sync needs a business channel linked to the app: 간편가입 cannot turn on without
one (kakaologin/prerequisite, 간편가입 사용 설정 requirements; console notice "간편가입
사용을 위해 비즈니스 채널을 연결해야 합니다"; DevTalk 151240/4). The channel-add line at
sign-up (`plusfriends`) is the optional part. A channel friend can receive channel
messages, so this is the CRM's cheapest repeat-contact list.

Sources:
- Channel guide (Kakao Business): https://kakaobusiness.gitbook.io/main/channel/start
- Connect a channel to an app: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/common#kakaotalk-channel-connect
- Channel FAQ in Kakao Sync: https://developers.kakao.com/docs/latest/ko/kakaosync/faq
- Channel relationship API: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#check-user-relationship

## Constraints to check first

- One business channel links to ONE biz app only. A channel linked to another app does
  not appear in the list. (kakaosync/faq) Another service needs its own channel, or the
  channel must move, which changes nothing for friends but breaks the old app's channel
  features.
- The app and the channel must carry the same business registration number. Change the
  number in Kakao Business > 비즈니스 설정 > 사업자 정보 관리.
- Roles: 마스터 or 매니저 on the channel, Owner or Editor on the app.
- A dormant, sanctioned or pending-delete channel cannot link.
- Some business types cannot become business channels (대부업, 성인용품, 주류, 담배, 청소년
  유해 업종). (kakaotalk-channel/common)

## Step 1. Create the channel (Kakao Business)

Get the channel name and 검색용 ID approved in the intake (section E5); the ID can never change.
The flow below was walked on 2026-11-25 (auto-fde, `_iaevX`).

1. Open https://business.kakao.com/profiles (내 비즈니스) in ego-browser. The page is shadow DOM;
   the creation wizard is a same-origin iframe. Read it through the snapshot tree.
2. [+ 새 비즈니스 만들기] > 유형1 기본 채널형 (radio card) > [다음].
3. "사업자 정보가 있나요?" > [네, 지금 입력할게요] > business number > [다음].
4. "같은 사업자등록번호로 운영 중인 채널이 있어요" lists existing channels with masked master
   emails. For a new product, press [새 채널 만들기].
5. 채널 정보: 프로필 사진 (640x640, JPG/PNG, 10 MB), 채널 이름 and 검색용 ID are prefilled with the
   company name. Replace both. **검색용 ID can never change.** 채널 이름 can change once, before
   business conversion and while friends ≤ 100. 카테고리 is suggested from the business record.
6. Adult-content question: [전 연령이 이용 가능한 채널이에요] for normal services.
7. "채널을 만들었어요": the channel is a 일반 채널, private and not searchable by default. Leave it
   private until the service is ready, but it must be public before it can be 대표 채널.

## Step 2. Business channel review (비즈니스 채널 심사)

Gate: run this step only when intake C9 says the service is formally launched. Kakao Business
rejects CBT, OBT and incomplete sites ("정식 사업 미개시", see `rejection-reasons.md` 3).

The agent does every step except the last one. Seen 2026-11-25 (법인, 대표자):

1. [비즈니스 채널로 전환] > "나는 사업자등록번호 …의" 대표자예요 / 직원이에요 / 업무를 대행하고 있어요.
2. 33%: "사업자등록증을 제출해 주세요" > [서류 추가] (up to 10 files). Upload the intake file B3
   from its original path with a file chooser. Do not copy it. A 법인 certificate has no
   대표자 주민등록번호; the 법인등록번호 is public and needs no masking.
3. 39%: Kakao reads the certificate and fills 업체명, 대표자명, 업태, 종목, 주소, 개업연월일.
   Compare each field with the certificate. Change nothing that matches.
4. 83%: "사업자 정보와 다르게 입력한 내용을 확인해 주세요" if the channel name differs from 상호.
   The channel name shows "수정 불가". [다음].
5. 88%: "사업자 정보와 다른 이유를 알려주세요". Fill 사유 (intake E6) and 링크 (the service URL).
   사유 accepts only 한글, 영문, 숫자, ( ) & . , - ~ / and spaces: a URL there fails on the colon.
   `page.fill` may refuse Korean here: click the textarea, then `keyboard.insertText`.
6. 94%: if the certificate lists a licensed 업종, "추가 서류 제출이 필요해요" asks for its license
   (예: 부동산 투자자문업 → 중개사무소 개설 등록증). Choose from intake B5a.
7. 99%: "나는 제출한 정보로 채널을 운영할 권리를 직접 갖고 있거나 회사로부터 위임받았으며, 입력한
   정보가 정확함을 확인했습니다." checkbox and [동의]. This is the owner's own attestation. Stop
   here and hand off (`handoffs-ko.md` 4). No 휴대폰 본인인증 or 전자증명서 screen appeared before
   this step. What follows [동의] is not yet recorded; record it on the next run.

The wizard saves each step ("입력한 정보가 저장됐어요").
To resume later: channel settings > [비즈니스 심사] > [채널 심사 신청하기] reopens the wizard at the
step where it stopped. That page lists what the person needs: 사업자등록증 or 고유번호증, a phone that can
receive a KakaoTalk 전자증명서, and an industry license if the business needs one. Documents depend on who applies (Kakao Business guide 2-2):

| Applicant | Must submit |
|---|---|
| 개인사업자 대표 | 본인 명의 카카오톡 전자증명서 |
| 법인사업자 대표 | 사업자등록증, 대표자 휴대폰 본인인증 |
| 직원 | 사업자등록증, 본인 명의 카카오톡 전자증명서 |
| 대행사 | 광고주·대행사 사업자등록증, 업무 대행 계약서 또는 위임장 |

Rules from the guide:
- Files: jpg, jpeg, png, pdf; 10 MB each, 100 MB total.
- The document must match the business number. Mask personal data. Low resolution or a
  cut-off image can be rejected.
- If the channel name differs from the company name on the registration (예: 서비스명 auto-fde vs 상호 리텐션 주식회사), write the reason in 사업자정보 불일치 소명 (under 300 characters).
  One of 사유, 링크 or 파일 is required. Give the website whose footer shows 상호 and 사업자등록번호.
- Education, food, medical, lodging and similar businesses must attach their license
  (업종별 인허가 서류). Check whether the service needs one before you submit.
- Review: about 3-5 business days, by Kakao Business, not Kakao Developers.

Hand off with section 4 of `handoffs-ko.md` (마지막 확인과 인증).

## Step 3. Link the channel to the app

1. Console: 앱 > 추가 기능 신청 > 추가 기능 > 카카오톡 채널 연결 > 신청.
2. Pick the channel. Review: 3-5 business days (developers.kakao.com reviewer).
3. After approval: 카카오 로그인 > 동의항목 > 대표 채널 > pick it. Without a 대표 채널,
   the consent screen has no channel-add line.

## Step 4. Turn on plusfriends

1. 카카오 로그인 > 동의항목 > 카카오톡 채널 추가 상태 및 내역 (`plusfriends`) > 설정.
2. Set 선택 동의 and a purpose (예: 카카오톡 채널 소식 안내). The item is only available
   after a channel is linked. (kakaotalk-channel/common)
3. Channel-add cannot be forced. Kakao: "채널 추가 항목은 사용자가 선택할 수 있는 항목입니다."
   (kakaosync/faq). Staff on DevTalk: "동의 자체는 광고 동의이므로 법적으로 불가합니다."
   (148458/14, 2026-02-24). Set plusfriends to 선택 동의.
3a. What the user agrees to: with a 대표 채널, the consent screen shows "[선택] {앱이름}의
   광고와 마케팅 메시지를 카카오톡으로 받습니다." That covers channel messages. The
   `plusfriends` scope only lets the app read the relationship and is not ad consent
   (DevTalk 134210/4). SMS, email and other ad sends still need the 광고성 정보 수신 동의
   term (`ad-consent-rules.md`).
3b. The channel shown on the service's screens must be the channel you link. Kakao
   rejected a link where they differed (DevTalk 150040/4). A live channel linked to a test
   app blocks linking it to the live app; unlink it there first (142570/18).
4. The line does not appear for a user who already follows the channel or whose Kakao
   account has no KakaoTalk.

## Step 5. Read the relationship in the app

```bash
curl -G "https://kapi.kakao.com/v2/api/talk/channels" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d "channel_ids=${CHANNEL_PUBLIC_ID}" \
  -d "channel_id_type=channel_public_id"
```

- `relation` is `ADDED`, `BLOCKED` or `NONE`. `created_at` comes only with ADDED.
- Needs the user's consent to `plusfriends`. Without it, the call fails; ask again with
  the additional-consent flow (`scope=plusfriends`).
- A user without KakaoTalk gets HTTP 400, code -501.
- Server-side batch check: the same endpoint with `Authorization: KakaoAK ${ADMIN_KEY}`,
  `target_id_type=user_id`, `target_id=<member id>`.
- To follow later changes, register 앱 > 웹훅 > 카카오톡 채널 웹훅 (add and block events).
- Store the result per member (relation, created_at, checked_at) so the CRM can segment by it.

## Developer channel (for test apps)

Kakao Business > 내 비즈니스 > [개발자용 채널 만들기] (shown only when you own at least one business
channel). Walked on 2026-11-25 (`_IxievX`):

- Name: 15 characters, Korean/English/digits only, no hyphen, never changes. Korean input did not
  take in the automated browser; use English (예: `autofdedev`).
- Category: two dropdowns (예: IT > 정보통신/SW). 소개 defaults to "테스트 용도입니다."
- It is not searchable in KakaoTalk, and it is created private. Press [공개 설정하기] on its dashboard,
  or the console refuses it as 대표 채널.
- Link it to the test app only (instant, no review). In the consent screen it shows as
  "(테스트)<name>".
