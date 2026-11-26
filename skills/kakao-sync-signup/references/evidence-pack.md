# Evidence pack for the 개인정보 동의항목 review

The request form takes ONE file at [E] 회원가입 화면: JPG, JPEG, PNG or PDF, 20 MB or
less. Build one PDF that walks the reviewer through 가입 → 로그인 → 탈퇴.

Sources:
- Form fields: https://developers.kakao.com/docs/latest/ko/kakaologin/prerequisite#additional-features
- Checklist: https://developers.kakao.com/docs/latest/ko/kakaologin/prerequisite#additional-feature-request-checklist
- Rejections "회원가입 증빙자료 미비", "개인정보 마스킹", "화면 오등록": https://developers.kakao.com/docs/latest/ko/kakaologin/faq#reject-reason

## Pages, in order

| # | Screen | Must show |
|---|---|---|
| 1 | Service landing or sign-up page | Service name, Kakao login button, company name in footer |
| 2 | Kakao consent screen | Each requested item with (필수) or (선택), the service terms, the channel-add line if used |
| 2a | Own sign-up form (only if intake item 16 = yes) | That form's fields with visible 필수 markers, or its validation error (DevTalk 140759/4, 152239/2). Items must match the request |
| 3 | Service terms list | The three terms with 필수/선택 |
| 4 | After sign-up | The member area: proves sign-up completed |
| 5 | Log-in again | The same Kakao button leads back to the member area |
| 6 | Withdrawal | The 회원 탈퇴 button and its confirm screen |
| 7 | Privacy policy | The section listing items, purpose (회원가입), 필수/선택 |

Put a one-line Korean caption above each screenshot, for example
"2. 카카오 동의 화면: 이름·전화번호·이메일 필수, 성별·출생 연도·채널 추가 선택".

If screens 4-6 do not exist yet, the form accepts a plan or design mock-up. Say so in
the caption.

## Getting screen 2 without real data

Use 카카오 로그인 > 간편가입 > 동의 화면 미리보기 in the console. It opens a dialog
with the real layout. Two things in that view are personal data: the signed-in admin's
email inside the preview, and the admin's name in the console header.

How the preview is built (tested on a live app, 2026-11-24): the dialog holds a
cross-origin iframe `https://kauth.kakao.com/support/preview?client_id=…&email=<admin
email>&lang=ko`. Text replacement in the console page cannot reach it. Replace the `email`
query value in the iframe's `src`, and hide the console header. This only changes what
the browser shows; nothing is saved. Never print the iframe URL: `client_id` is the app's
REST API key.

```js
// ego-browser script, after the preview dialog is open. Tested 2026-11-24.
await page.evaluate(() => {
  const f = [...document.querySelectorAll("iframe")]
    .find((x) => x.src.includes("kauth.kakao.com/support/preview"));
  const u = new URL(f.src);
  u.searchParams.set("email", "user@example.com");
  f.src = u.toString();
  [...document.querySelectorAll('header, nav, [class*="gnb" i], [class*="header" i]')]
    .filter((e) => !e.contains(f))
    .forEach((e) => { e.style.visibility = "hidden"; });
});
await page.waitForTimeout(2500); // the iframe reloads
await page.screenshot({ path: "/absolute/path/02-consent.png" });
```

Then open the PNG and check by eye that no email or name is left.

What did not work in the same test, so do not rely on it:
- Text-node replacement: reported 0 emails left, but the screenshot still showed the
  email (it lives in the iframe).
- Opening the preview URL on its own page: Kakao answers "잘못된 요청 (KOE001)".
- Cropping with `getBoundingClientRect()` as `clip`: the console page scales its layout,
  so the crop landed off target. Use the full screenshot.
- `mouse.wheel` over the preview: the inner list did not scroll.

What works for the whole screen (tested 2026-11-25): after the email swap, set the iframe's
`style.height = "1150px"` and clear `max-height`/`overflow` on its parents, then take a full-page
shot and crop the dialog. `docs/screenshots/2026-11-25-auto-fde/28-test-consent-full.png` shows the
Kakao items, the three terms and the channel-add line in one image.

For screens 4-6, sign in with a test account. Mask its name, email, phone and member ID
with text replacement on the service's own pages (same origin), then check each PNG.

## Building the PDF

1. Write an HTML page with the captions and `<img>` tags (absolute `file://` paths), one
   screen per page (`page-break-after: always`). Give images `max-width:100%;
   max-height:90vh` so one screenshot does not spill over two pages.
2. Open it in ego-browser (`page.goto("file:///absolute/path/evidence.html")`) and print
   it with CDP. Tested 2026-11-24: a one-screen test PDF came out at 62 KB.

```js
const { data } = await page.cdp("Page.printToPDF", { printBackground: true, preferCSSPageSize: true });
const fs = await import("node:fs/promises");
await fs.writeFile("/absolute/path/kakao-signup-evidence.pdf", Buffer.from(data, "base64"));
```

3. Check: size under 20 MB, every page readable, no unmasked personal data. Look at each
   page image yourself before upload; do not sample.

## Upload

The upload is a file chooser in the request dialog. Use
`page.waitForFileChooser()` before the click, then `chooser.setFiles(<pdf path>)`.
Do this only after the intake write grant and a PASS from `review-checklist.md`.
