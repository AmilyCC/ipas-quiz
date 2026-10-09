# iPAS 初級刷題室

iPAS AI 應用規劃師（初級）刷題網站。純靜態網頁，一個 `index.html` 就能跑，可以直接放上 GitHub Pages。

- 歷屆公告試題 400 題（114 年第四次、115 年第一～三次，科目一、科目二）
- 學習指引練習題 69 題（含官方解析，已套用勘誤表）
- 練習模式（即時對答）、計時模擬考、錯題本、收藏、學習指引重點整理
- 作答紀錄先存在瀏覽器，登入後可同步到自己的 Google 雲端硬碟（隱藏的應用程式資料夾），換裝置也能接著刷
- 每題附官方 PDF 出處連結與頁碼；學習指引練習題另附官方解析頁碼

## Google 登入

網站用 Google Identity Services 做登入，只有 `config.json` 裡 `allowedEmails` 列出的帳號能進入。

- `googleClientId`：Google Cloud 專案 `ipas-quiz` 的 OAuth 網頁用戶端 ID（已授權來源 `https://amilycc.github.io`）
- `allowedEmails`：允許登入的 Google 帳號
- OAuth 同意畫面目前是「測試」狀態，新增帳號時也要到 Google Cloud 控制台 → Google Auth Platform → 目標對象 → 測試使用者 加入同一個信箱
- 登入狀態保留 30 天；改完 `config.json` 後執行 `python build.py`
- `googleClientId` 設為 `null` 會關閉登入，網站直接開放使用

### 雲端硬碟同步

登入時會一併請你授權 Google 雲端硬碟（範圍只有 `drive.appdata`，網站讀不到雲端硬碟裡的其他檔案），登入後自動同步，不用另外按按鈕。紀錄存成 `ipas-aiap-progress.json`，放在雲端硬碟的隱藏應用程式資料夾，不會出現在檔案列表。

每次同步都是「先下載雲端紀錄 → 和這台裝置合併 → 再上傳」，不會用某台裝置的舊資料蓋掉其他裝置的進度。作答後約 1.5 秒自動同步；另外回到分頁時、以及開著網頁時每 60 秒，會自動抓一次其他裝置的新進度。錯題本和收藏會記下每次加入／移除的時間，合併時以最新的動作為準。

雲端硬碟的授權約 1 小時過期。續期需要開 Google 視窗，瀏覽器只允許在點擊時開啟，所以過期後右上角會顯示「☁ 點此同步」：點它（或點頁面任何地方）就會重新連線並同步，期間的作答會先存在本機。若沒有跳出視窗，請允許此網站的彈出式視窗。Google Cloud 專案需啟用 Google Drive API。

這是前端的登入門檻：題庫檔案仍在公開的 repository 裡，登入不會保護題目內容。

## 部署到 GitHub Pages

1. 在 GitHub 建立新的 repository（例如 `ipas-quiz`），可選 Public 或 Private（Private 需付費方案才能開 Pages）。
2. 把這個資料夾的所有檔案上傳到 repository 根目錄：
   - 網頁操作：repository 頁面 → **Add file → Upload files** → 把檔案拖進去 → **Commit changes**
   - 或用指令：
     ```bash
     git init
     git add .
     git commit -m "iPAS 初級刷題室"
     git branch -M main
     git remote add origin https://github.com/<你的帳號>/ipas-quiz.git
     git push -u origin main
     ```
3. 到 repository 的 **Settings → Pages**，Source 選 **Deploy from a branch**，Branch 選 `main`、資料夾選 `/ (root)`，按 **Save**。
4. 等 1～2 分鐘，網址會是 `https://<你的帳號>.github.io/ipas-quiz/`。

也可以直接拖到 Netlify Drop（app.netlify.com/drop）或 Cloudflare Pages，一樣不需要設定。

## 檔案結構

```
index.html            網站本體（題庫與重點已內嵌，可離線開啟）
data/questions.json   題庫（469 題）
data/notes.json       重點整理
src/template.html     網頁模板
config.json           Google 登入設定（用戶端 ID、允許帳號）
build.py              修改 data/ 或 config.json 後重新產生 index.html
.nojekyll             讓 GitHub Pages 原樣輸出檔案
```

## 新增或修正題目

編輯 `data/questions.json`，每題格式：

```json
{"id":"e115-3-1-1","src":"exam","sess":"115-3","subj":1,"n":1,
 "q":"題目","o":["選項A","選項B","選項C","選項D"],"a":["B"],"e":"解析（可留空）"}
```

- `src`：`exam`（歷屆試題）或 `guide`（學習指引）
- `sess`：場次，例如 `115-3`；新場次需同時加到 `src/template.html` 的 `SESS` 清單
- `a`：正確答案，可多個（如 `["A","C"]`）

改完執行 `python build.py` 重新產生 `index.html`，再 commit 上傳。

## 資料來源

題目與學習指引內容取自經濟部產業發展署 iPAS〈AI 應用規劃師 學習資源〉公開下載的初級公告試題與學習指引：
https://ipd.nat.gov.tw/ipas/certification/AIAP/learning-resources

著作權屬原單位所有，本站僅供個人備考練習。公開分享前請留意原網站的使用規範。考試資訊請以官方簡章為準。
