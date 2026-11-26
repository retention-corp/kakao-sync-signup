# Ad consent (광고성 정보 수신 동의)

Use this when the service will send marketing by KakaoTalk, SMS, email or app push.
The ad-consent term is how the CRM proves it may message a member.

## Sources

- KISA, 「불법스팸 방지를 위한 정보통신망법 안내서」 7th revision, KISA-GD-2025-0037,
  2025-12, section "바. 명시적인 사전동의". Page numbers below are PDF pages; each PDF page holds two printed pages. Download:
  https://www.kisa.or.kr/2060301/form?postSeq=19 (attachment "(7차 개정) 불법스팸 방지를 위한 정보통신망법 안내서.pdf")
- KISA press release, 2026-03-04: https://www.kisa.or.kr/402/form?postSeq=2577
- Kakao Login service-terms policy: https://developers.kakao.com/docs/latest/ko/kakaologin/common#policy-terms
- Kakao service-terms fields: https://developers.kakao.com/docs/latest/ko/kakaologin/prerequisite#service-terms
- Service terms API: https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#get-service-terms

## Rules

### 1. The title says "광고성 정보 수신 동의"

KISA PDF p.8: "동의를 받을 때에는 이용자가 광고라는 사실을 인지할 수 있도록 "광고성 정보
수신동의"임을 명확하게 표시하여야 하며, 광고가 아닌 것으로 오인할 수 있는 형태(정보제공
동의, 혜택알림 동의, 마케팅 동의 등)로 수신동의를 받은 경우 명시적인 사전 동의를 받은
것으로 볼 수 없습니다."

- Use `광고성 정보 수신 동의` at the start of the Korean title.
- Add the media in brackets: `광고성 정보 수신 동의(카카오톡·문자·이메일)` (25 characters;
  Kakao's limit is 45).
- Invalid titles: 마케팅 동의, 마케팅 활용 동의, 혜택 알림 동의, 이벤트 알림, 정보제공 동의,
  소식 받기.
- Note: Kakao's own doc uses "마케팅 활용 동의" as an example term name
  (kakaosync/common). That example predates the KISA rule. Follow KISA.

### 2. It is a separate, optional term

- KISA PDF p.8: putting ad consent inside the terms of service "명시적인 동의를 받은 것으로 볼
  수 없습니다". Register it as its own term.
- KISA PDF p.8: personal-data consent and ad-receipt consent "각 동의는 별개로 받아야 합니다".
- Set 동의 단계 to 선택 동의. A required ad consent forces it as a sign-up condition, which
  is not a free choice.

### 3. Never pre-checked

- KISA PDF p.8: "체크 박스에 "동의"를 "기본값(default)로 설정해 두었다면, 명시적인 사전 동의를
  받은 것으로 볼 수 없습니다."
- Kakao's consent screen does not pre-check optional items (seen in the 2026-11-24 preview
  of a live app: optional rows unchecked, a note that 전체 선택하기 includes optional items).
- Your own site must follow the same rule wherever it asks again (profile page, checkout).

### 4. Name the media, and let the user pick

- KISA PDF p.8 recommends a per-medium choice, with the KakaoTalk example
  "□ SNS/메신저/플랫폼 ( □ 카카오톡 …)". A message may go only to the media agreed.
- Kakao terms are one checkbox each. Either list the media in the title and on the term
  page, or register one term per medium. One term with the media listed is the pattern
  in production at a live service (tag pattern `ad_consent_<YYYYMMDD>`).

### 5. The term page is live before you register the term

- Kakao requires the registered term to equal the real term: "앱에 등록한 서비스 약관의
  내용은 실제 서비스 약관과 동일해야 하며 관련 법률을 준수해야 합니다."
  (kakaologin/common#policy-terms)
- The page must state: the sender's name, what ads are sent, the media, that consent is
  optional, and how to withdraw it.
- `scripts/precheck.py` fetches the URL and fails if it does not return 200 or does not
  contain "광고성 정보".

### 6. The tag is what the app reads

- Tag format: letters, digits, `-`, `_`. Use `ad_consent_<YYYYMMDD>`.
- When the term text changes in substance, register a new term with a new date tag and
  turn the old one OFF. Members who agreed to the old tag stay recorded under it.
- Read it back (see `api-readback.md`):

```bash
curl -G "https://kapi.kakao.com/v2/user/service_terms" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -d "tags=ad_consent_20261119"
```

  Treat the member as consented only when the returned term has `agreed: true`. Store
  `agreed_at` and `agreed_by` as the proof KISA asks for ("전송자는 수신자로부터 명시적인
  사전동의를 받았다는 것을 증명할 수 있어야 합니다", PDF p.8).

### 7. Duties after consent (the CRM must schedule these)

- Within 14 days of a consent, refusal or withdrawal, tell the member the result (KISA
  PDF p.13-14, "14일 이내"; a missed notice can bring a fine of up to 10 million won).
- Every 2 years from the consent date, tell the member that they consented (KISA PDF
  p.14, "수신동의를 받은 날부터 2년마다").
- Every ad message starts with "(광고)" and states the sender, and opting out must be
  easy (KISA PDF p.21-22). Read that section before the first send.

These are CRM duties, not console steps. Put them in the report as open items with an
owner.
