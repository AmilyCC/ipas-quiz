# iPAS 初級刷題室

iPAS AI 應用規劃師（初級）刷題網站。純靜態網頁，一個 `index.html` 就能跑，可以直接放上 GitHub Pages。

- 歷屆公告試題 400 題（114 年第四次、115 年第一～三次，科目一、科目二）
- 學習指引練習題 69 題（含官方解析，已套用勘誤表）
- 練習模式（即時對答）、計時模擬考、錯題本、收藏、學習指引重點整理
- 作答紀錄存在瀏覽器的 localStorage，不需要帳號或後端

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
build.py              修改 data/ 後重新產生 index.html
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
