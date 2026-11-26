// console-helpers.mjs — small, tested helpers for the Kakao Developers console in ego-browser.
// Import inside an `ego-browser nodejs` script:
//   const H = await import("/abs/path/skills/kakao-sync-signup/scripts/console-helpers.mjs");
// Each helper checks the app ID in the URL first, so a write never lands in the wrong app.

export function assertApp(url, appId) {
  if (!url.includes(`/console/app/${appId}/`)) throw new Error(`refusing to write: page is not app ${appId}`);
}

// Scroll an element inside a dialog or a list into view. Console dialogs and dropdowns scroll on
// their own; the browser's automatic scroll does not reach inside them ("not visible in the viewport").
export async function scrollTextIntoView(page, text, scope = "body") {
  return page.evaluate(([t, s]) => {
    const root = document.querySelector(s) || document.body;
    const el = [...root.querySelectorAll("*")].find((e) => e.children.length === 0 && e.textContent.trim() === t);
    if (el) el.scrollIntoView({ block: "center" });
    return !!el;
  }, [text, scope]);
}

// Open the 설정 dialog of one consent item by its exact ID (예: "name").
// Substring matching is wrong: "name" also matches "profile_nickname".
export async function openScope(page, appId, scopeId) {
  assertApp(await page.url(), appId);
  const ok = await page.evaluate((id) => {
    const row = [...document.querySelectorAll("tr")].find((r) => [...r.querySelectorAll("td")].some((td) => td.innerText.trim() === id));
    const btn = row && [...row.querySelectorAll("button")].find((b) => b.innerText.trim() === "설정");
    if (!btn) return false;
    document.querySelectorAll("[data-scope-btn]").forEach((b) => b.removeAttribute("data-scope-btn"));
    btn.setAttribute("data-scope-btn", id); btn.scrollIntoView({ block: "center" }); return true;
  }, scopeId);
  if (!ok) throw new Error(`no 설정 button for scope ${scopeId} (권한 없음?)`);
  await page.click(`button[data-scope-btn="${scopeId}"]`, { label: `open ${scopeId} settings` });
  await page.waitForSelector("[role=dialog] input[name=purpose]", { timeout: 5000 });
  const head = await page.evaluate(() => document.querySelector("[role=dialog]").innerText);
  if (!head.includes(`/ ${scopeId}`)) throw new Error(`dialog opened for the wrong item: ${head.split("\n")[2]}`);
}

// level: "REQUIRED" | "OPTIONAL" | "LAZY" | "NONE". collect: turn on 카카오계정으로 수집 후 제공 (필수 only).
export async function setScope(page, appId, scopeId, level, purpose, { collect = false } = {}) {
  await openScope(page, appId, scopeId);
  await page.click(`[role=dialog] button[value=${level}]`, { label: `choose ${level}` });
  await page.waitForTimeout(300);
  if (collect) {
    const on = await page.evaluate(() => document.querySelector('[role=dialog] button[value=on]')?.getAttribute("aria-checked"));
    if (on === "false") await page.click("[role=dialog] button[value=on]", { label: "turn on 수집 후 제공" });
  }
  if (level !== "NONE") await page.fill("[role=dialog] input[name=purpose]", purpose);
  await scrollTextIntoView(page, "저장", "[role=dialog]");
  const ref = (await page.snapshot()).match(/dialog "동의항목 설정" \[ref=(\d+)/)[1];
  const sub = await page.snapshot({ scope: "subtree", root: "@" + ref });
  await page.click("@" + sub.match(/button \[ref=(\d+)[^\n]*\]\n\s+text "저장"/)[1], { label: `save ${scopeId}` });
  await page.waitForTimeout(1500);
  const leftover = await page.evaluate(() => [...document.querySelectorAll("[role=dialog],[role=alertdialog]")].map((d) => d.innerText).join(" | "));
  return leftover;
}

export async function scopeStates(page) {
  return page.evaluate(() => Object.fromEntries([...document.querySelectorAll("tr")].map((r) => {
    const tds = [...r.querySelectorAll("td")].map((td) => td.innerText.trim()); return tds.length >= 3 ? [tds[1], tds[2]] : null;
  }).filter(Boolean)));
}

// Add one service term on 카카오 로그인 > 간편가입. The [서비스 약관 추가] dialog must already be open,
// or pass open=true. term = { title_ko, title_en, url, required, tag }.
export async function addTerm(page, appId, term, { open = true } = {}) {
  assertApp(await page.url(), appId);
  if (open) {
    const snap = await page.snapshot();
    await page.click("@" + snap.match(/button \[ref=(\d+)[^\n]*\]\n\s+text "서비스 약관 추가"/)[1], { label: "add service term" });
    await page.waitForSelector("[role=dialog] input[name=title_ko]", { timeout: 5000 });
  }
  await page.fill("[role=dialog] input[name=title_ko]", term.title_ko);
  await page.fill("[role=dialog] input[name=title_en]", term.title_en);
  if (term.url) await page.fill("[role=dialog] input[name=url]", term.url);
  await page.click(`[role=dialog] button[value="${term.required ? "true" : "false"}"]`, { label: term.required ? "필수" : "선택" });
  await page.fill("[role=dialog] input[name=tag]", term.tag);
  const got = await page.evaluate(() => Object.fromEntries([...document.querySelectorAll("[role=dialog] input")].map((i) => [i.name, i.value])));
  for (const k of ["title_ko", "title_en", "tag"]) if (got[k] !== term[k]) throw new Error(`field ${k} did not take the value: ${got[k]}`);
  await scrollTextIntoView(page, "저장", "[role=dialog]");
  const ref = (await page.snapshot()).match(/dialog "서비스 약관 추가" \[ref=(\d+)/)[1];
  const sub = await page.snapshot({ scope: "subtree", root: "@" + ref });
  await page.click("@" + sub.match(/button \[ref=(\d+)[^\n]*\]\n\s+text "저장"/)[1], { label: `save term ${term.tag}` });
  await page.waitForTimeout(1500);
  return page.evaluate(() => [...document.querySelectorAll("[role=dialog],[role=alertdialog]")].map((d) => d.innerText).join(" | "));
}
