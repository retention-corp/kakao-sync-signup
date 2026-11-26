# App code: sign-up and readback

What the service code must do so that the console setup turns into CRM data.

Sources:
- REST API: https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api
- Sign-up flow checks: https://developers.kakao.com/docs/latest/ko/kakaosync/faq
- Policy (unlink, destruction, 24-hour rule): https://developers.kakao.com/docs/latest/ko/kakaologin/common#policy


## 1. Authorize

```
GET https://kauth.kakao.com/oauth/authorize
  ?response_type=code&client_id=${REST_API_KEY}&redirect_uri=${REDIRECT_URI}&state=${STATE}
```

- `state`: unique per request; check it on return (CSRF).
- `scope`: do not send it on first sign-up. The doc defines it for additional consent
  ("동의항목 추가 동의 요청 시 사용"). Its effect (kakaologin/utilize, 인가 코드 요청 API의 scope
  파라미터 table):
  - 미포함: "앱에 [필수 동의] 또는 [선택 동의]로 설정된 동의항목으로 구성된 동의 화면 표시"
  - 포함: "scope 파라미터에 포함한 동의항목만으로 구성된 동의 화면 표시"
  So a `scope` list silently drops every console item it omits. One live app sent
  `scope=account_email,phone_number,name,plusfriends`; gender and birthyear were 선택 in the
  console and in its privacy policy, but no member was ever asked for them. Grep the
  authorize URL code for `scope` in phase 6, and make code, console and policy agree.
- `service_terms`: only to ask for specific terms later; it must include at least one
  필수 term or no screen appears. Do not send it on first sign-up.
- With OpenID Connect ON, any `scope` request must include `openid`.

## 2. Token and user

1. `POST https://kauth.kakao.com/oauth/token` with `grant_type=authorization_code`,
   `client_id`, `client_secret` (ON by default), `redirect_uri`, `code`. Put the secret in
   the form body, never in the URL.
2. `GET https://kapi.kakao.com/v2/user/me` with `Authorization: Bearer`.
3. Key the member on `id` (회원번호). It survives withdrawal and re-join while
   사용자 아이디 고정 is on (it is on by default; shown on 카카오 로그인 > 고급). Email and
   phone change; do not key on them.
4. Treat a field as present only when its `*_needs_agreement` is false and the value
   exists. A 필수 item can still be empty: "[필수 동의]는 ... 카카오계정에 없는 값을 카카오가
   생성해 제공한다는 의미는 아닙니다." (kakaosync/faq)
5. Phone: empty for Kakao accounts without KakaoTalk. Ask for it on the service page or
   proceed without it.
6. Email: use it only when `is_email_valid` and `is_email_verified` are true.

Call a user-info API within 24 hours of the first login, or Kakao unlinks the user as an
unfinished sign-up (rule since 2020-12-28).

## 3. Terms readback

```
GET https://kapi.kakao.com/v2/user/service_terms?tags=${TAG1},${TAG2}
Authorization: Bearer ${ACCESS_TOKEN}
```

- Response: `service_terms[]` with `tag`, `required`, `agreed`, `revocable`, `agreed_at`
  (UTC, RFC3339), `agreed_by` (`KAUTH` = sign-up screen, `KAPI` = API).
- `result=app_service_terms` lists every active term in the app, agreed or not.
- An unknown tag returns HTTP 400 with code -2. Keep tags in config, and alert on -2.
- Server-side with admin key: add `target_id_type=user_id&target_id=${USER_ID}` and
  `Authorization: KakaoAK ${ADMIN_KEY}`.
- Store per member: tag, agreed, agreed_at, agreed_by. The ad-consent row is the CRM's
  proof of opt-in (see `ad-consent-rules.md`).
- Check required terms before you create the member (kakaosync/faq sign-up flow).

## 4. Channel readback

See `channel-steps.md` Step 5 (`GET /v2/api/talk/channels`).

## 5. Withdrawal and unlink

1. On 회원 탈퇴, call `POST https://kapi.kakao.com/v1/user/unlink`, then delete the member's
   data, including the Kakao member ID, unless the member agreed to retention.
2. Register 앱 > 웹훅 > 연결 해제 웹훅 (or 계정 상태 변경 웹훅) so the service also learns
   about unlinks done outside the service. The console warns when neither is set.
   A live app checked on 2026-11-24 had neither registered.
   Spec (kakaologin/callback, read 2026-11-25):
   - Method GET or POST. Parameters `app_id`, `user_id`, `referrer_type` (`ACCOUNT_DELETE`,
     `FORCED_ACCOUNT_DELETE`, `UNLINK_FROM_ADMIN`, `UNLINK_FROM_APPS`, `INCOMPLETE_SIGN_UP`).
   - Header `Authorization: KakaoAK ${PRIMARY_ADMIN_KEY}`. Compare it with the 대표 어드민 키, and
     compare `app_id` with your app ID.
   - "HTTP 상태 코드 200 OK 로 3초 내에 응답해야 합니다. 사용자 정보가 없거나 오류 발생 시에도
     200 OK 으로 응답해야 합니다."
   - Kakao does not send it when the service itself called `POST /v1/user/unlink`.
   Before you write the handler, find the service's existing withdrawal path. The webhook
   only calls it. If the service has no withdrawal path, stop: the deletion policy (orders
   kept for 5 years under 전자상거래법, what to anonymize, audit rows) is the owner's
   decision, not the agent's. Ask for it in the intake (section D).
   The service also needs the 대표 어드민 키 in its server env. Only the app Owner can see it.
   Move it with the no-print pattern in `console-steps.md` Step 7.
   Testing: do not press [전송] in 도구 > 웹훅 테스트 > 연결 해제 on a live app. It sends the
   signed-in Kakao account's own member ID (seen 2026-11-26), so a working handler deletes the
   tester's real membership. Test instead with the real key and a member ID that does not exist:
   expect 200 and an "unknown user" log line; a wrong `app_id` must give 401.
   Register it at 앱 > 웹훅 > 연결 해제 웹훅 > [웹훅 등록]: 상태 사용함, 메서드 GET (the dialog default),
   URL. Read the card back after saving.
3. Unlinking does not remove the channel friendship. A member who withdraws keeps getting
   channel messages until they block the channel (kakaosync/faq).

## 6. Existing Kakao Login members

If the app already used Kakao Login before Kakao Sync, the member ID stays the same.
Look up by `id` first and update the existing member with the new fields and term
consents instead of creating a new member (kakaosync/faq).
