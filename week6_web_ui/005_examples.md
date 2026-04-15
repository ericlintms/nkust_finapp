# 實務範例與實作 (Week 6)

歡迎來到「看得見」的課程！我們要把之前算的冷冰冰數字，搬上漂亮的網頁！

## 系統要怎麼找到網頁檔案？

在使用 FastAPI 渲染網頁時，我們必須創立一個專門放 HTML 檔案的資料夾。
大家業界的默契，這個資料夾通常叫做 **`templates`** (模板資料夾)。請你一定要保持這個結構。

```
week6_web_ui/
├── examples/
│   ├── templates/          <-- (非常重要！放 html 的地方)
│   │   ├── w601_hello.html
│   │   └── w602_dashboard.html
│   ├── w601_first_page.py
│   └── w602_stock_dashboard.py
```

## 我們的練習清單

### 1. 例題一：Jinja2 參數傳遞魔法
- **對應檔案**: `examples/w601_first_page.py` 與 `examples/templates/w601_hello.html`
- **練習目的**: 了解 FastAPI 是怎麼透過 `Jinja2Templates` 把變數「注射」進 HTML 裡面的。
- **實作任務**:
  1. 切換目錄到 `week6_web_ui/examples/`。
  2. 如果還沒安裝，幫我執行：`pip install jinja2`。
  3. 啟動伺服器：`uvicorn w601_first_page:app --reload`。
  4. 打開瀏覽器，前往 `http://127.0.0.1:8000/hello/Elon`，然後再換成你自己的名字，看看網頁是不是會動態跟著你改變問候語？這就是 SSR！

### 2. 例題二：打造財經儀表板 (Dashboard)
- **對應檔案**: `examples/w602_stock_dashboard.py` 與 `examples/templates/w602_dashboard.html`
- **練習目的**: 綜合應用 Bootstrap 5 美化排版，把我們模擬的 Python 股票陣列清單，利用 `{% for %}` 迴圈渲染成一個專業的網頁表格。
- **實作任務**:
  1. 保持在同一個目錄。停掉剛才的伺服器 (按 `Ctrl+C`)。
  2. 啟動新的任務：`uvicorn w602_stock_dashboard:app --reload`。
  3. 打開瀏覽器前往首頁：`http://127.0.0.1:8000/`。
  4. 欣賞一下這個網頁！看看那個導航列、卡片與漂亮的斑馬紋表格！你可以打開 `.html` 檔案，試著把 `bg-dark` 改成 `bg-primary`，存檔後重新整理網頁，看看顏色的變化！
