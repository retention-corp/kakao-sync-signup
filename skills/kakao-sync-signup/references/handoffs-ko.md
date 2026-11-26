# Hand-off scripts (Korean)

The user reads these. Each one has: why, time, numbered steps with the URL and exact labels,
traps, and the exact reply to send back. Ask for everything known in advance in the intake;
hand-offs are only for moments a person must act live. Fill every `{…}` before sending. Before each hand-off:

1. Try the step yourself first. Hand off only what needs his login, phone, documents or
   approval.
2. Call `await task.handOff()` in the TaskSpace, and print the TaskSpace ID.
3. After his reply, `takeOverTaskSpace(<id>)` and check the result on screen. If it is not
   done, say what you see and send the step again.

## 1. 카카오 로그인 (세션 만료)

```text
1. 카카오디벨로퍼스 다시 로그인
   - 이유: 로그인이 풀려서 콘솔 설정을 이어갈 수 없어요.
   - 시간: 1분
   - 할 일:
     1. ego-browser에서 지금 열린 탭 "{탭 제목}"을 보세요.
     2. [카카오계정으로 로그인]을 누르고 평소처럼 로그인하세요.
     3. 휴대폰에 카카오톡 인증 알림이 오면 [확인]을 누르세요.
   - 주의: 다른 탭이나 다른 앱 화면으로 이동하지 마세요.
   - 끝나면 "로그인 완료"라고 보내 주세요. 제가 이어서 {다음 단계}를 진행해요.
```

## 2. 본인인증 (추가 기능 신청 자격)

```text
1. 카카오디벨로퍼스 계정 본인인증
   - 이유: 카카오가 "추가 기능 신청" 전에 계정 주인 본인인증을 요구해요. 이게 있어야 전화번호·이름 동의항목을 신청할 수 있어요.
   - 시간: 3분
   - 할 일:
     1. ego-browser 탭에서 https://developers.kakao.com 오른쪽 위 프로필 > [계정 설정]을 누르세요.
     2. [본인인증]을 누르세요.
     3. 휴대폰 번호 인증을 끝까지 진행하세요.
   - 주의: 인증 문자의 번호는 저에게 보내지 마세요.
   - 끝나면 "본인인증 완료"라고 보내 주세요. 제가 [신청 자격 확인] 화면을 다시 확인해요.
```

## 3. 비즈 앱 전환 (Owner가 아닐 때)

```text
1. {앱 이름} 비즈 앱 전환
   - 이유: 사업자 정보를 등록해야 채널 연결과 동의항목 신청이 열려요. 이 작업은 앱 Owner만 할 수 있어요. 지금 계정 역할은 {역할}이에요.
   - 시간: 3분
   - 할 일:
     1. Owner 계정({Owner 이름})으로 https://developers.kakao.com/console/app/{APP_ID}/config 를 여세요.
     2. [비즈니스 정보] > [사업자 정보 등록]을 누르세요.
     3. 사업자 구분 [국내 사업자]를 고르고 아래 번호를 넣으세요.
        {사업자등록번호}
     4. [저장]을 누르세요.
   - 주의: 앱 아이콘이 없으면 버튼이 막혀요. 아이콘은 제가 먼저 넣어 둘게요.
   - 끝나면 "비즈 앱 전환 완료"라고 보내 주세요. 제가 채널 연결 신청으로 넘어가요.
```

## 4. 채널 심사 마지막 확인 (서류·소명은 에이전트가 넣음)

```text
1. 카카오톡 채널 {채널 이름} 비즈니스 채널 심사 — 마지막 확인과 인증
   - 이유: 채널이 "비즈니스 채널"이어야 앱과 연결돼요. 서류·사업자 정보·소명은 제가 넣어 뒀어요. 마지막 확인란은 회사 명의의 확인이라 대표님이 직접 누르셔야 해요.
   - 시간: 3분 (심사는 영업일 3~5일)
   - 할 일:
     1. 브라우저 탭 "{탭 제목}"을 보세요. https://business.kakao.com/space/{space}/channel/{채널 ID}/settings/review 위에 "99% 완성" 창이 열려 있어요.
     2. 입력한 내용을 보려면 [이전]으로 돌아가 보세요. 고칠 곳이 없으면 99% 화면으로 돌아오세요.
     3. "나는 제출한 정보로 채널을 운영할 권리를 직접 갖고 있거나 …" 확인란을 체크하고 [동의]를 누르세요.
     4. 휴대폰 본인인증이나 카카오톡 전자증명서 화면이 나오면 끝까지 진행하세요.
     5. 심사 신청 완료 문구가 보이면 끝이에요.
   - 주의: 인증 문자·번호는 저에게 보내지 마세요. [다시 시작하기]는 누르지 마세요. 첫 단계로 돌아가요.
   - 끝나면 "채널 심사 신청 완료"라고 보내 주세요. 신청 날짜를 기록하고, 승인되면 앱-채널 연결을 신청할게요.
```

If the intake did not collect the documents (an older run), add these steps before step 3:
[서류 추가] → upload the certificate → [편집] to confirm masking. Then fix the intake for next time.

## 4b. 테스트 앱 실제 로그인 (테스트 앱을 만든 경우)

```text
1. 테스트 앱 실제 로그인 확인
   - 이유: 미리보기가 아니라 실제 동의 화면과 가입이 되는지 확인해요. 동의 버튼은 본인 계정이라 직접 누르셔야 해요.
   - 시간: 1분
   - 할 일:
     1. 브라우저 탭 "{탭 제목}"을 보세요. 테스트 앱의 카카오 로그인 화면이 열려 있어요.
     2. 동의 화면에서 필수 항목만 체크된 상태로 [동의하고 계속하기]를 누르세요.
     3. {콜백 주소} 화면으로 돌아오면 끝이에요.
   - 주의: 선택 항목(채널 추가, 광고성 정보)은 시험이라 체크하지 않아도 돼요.
   - 끝나면 "테스트 로그인 완료"라고 보내 주세요. 약관 동의 내역과 채널 관계를 API로 읽어 확인할게요.
```

## 5. 저장·심사 신청 승인 (입력값에서 승인을 못 받았을 때만)

```text
결정이 필요한 것: {앱 이름}(ID {APP_ID})에 아래 내용을 저장하고 카카오 심사를 신청할지
- 저장할 것: {변경 목록, 한 줄씩}
- 심사 신청: {개인정보 동의항목 / 채널 연결}
- 사전 점검: precheck {PASS n개 / WARN n개 / FAIL 0개}
- 추천: 승인. 이유: {한 줄}
승인하려면 이렇게 보내 주세요:
"{앱 이름} 저장·심사 신청 승인"
```

## 6. 카카오 심사 반려 후

```text
1. {앱 이름} 개인정보 동의항목 반려 대응
   - 반려 사유(원문): "{사유}"
   - 원인: {한 줄}
   - 제가 고칠 것: {목록}
   - 직접 정하실 것: {있으면 한 가지, 추천 포함 / 없으면 "없음"}
   - 다시 신청하려면 이렇게 보내 주세요: "{앱 이름} 재신청 승인"
```
