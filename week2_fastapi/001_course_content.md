# Week 2: 課程內容 (Course Content)

## 學習目標

第一週我們寫出的 Python 函數只能在自己的電腦黑畫面裡跑，這週我們要把它「開放給外部世界」存取！我們正式踏入 Web 的世界，用 FastAPI 這個框架建立最基礎的 API，了解現代網路架構的核心精神。

## 涵蓋主題

1. **API (Application Programming Interface)**
   - 什麼是 API？為什麼我們做財管系統會需要 API？
   - Web API 的運作哲學：伺服器 (算數字的地方) 與客戶端 (看畫面的地方) 的分工合作。

2. **HTTP 協定基礎**
   - 了解 HTTP Request (發出請求) 與 Response (收到回應)。
   - 常見的操作方法解密：GET (拿資料), POST (送資料)。
   - 那些神秘的狀態碼到底是什麼意思 (200 OK, 400 參數給錯, 404 找不到, 500 我們的程式寫炸了)。

3. **FastAPI 框架實作**
   - 在電腦上啟動我們人生第一個 FastAPI 伺服器 (`uvicorn`)。
   - 用 Decorators (裝飾器，像是加上 `@app.get`) 把網址跟我們的 Python 函數綁在一起。
   - 解析網址上帶進來的參數 (Query Parameters)。
   - 讓程式回傳 JSON 格式 (一種所有程式語言都看得懂的資料格式) 的計算結果。

## 本週預期產出

- 我能夠在自己的電腦上成功啟動一個 FastAPI 伺服器 (Port 8000)。
- 利用 FastAPI 自動幫我們生成的漂亮測試網頁 (Swagger UI) 進行功能測試。
- 做出一個能透過瀏覽器發送參數進去、並算好財管數值回傳給我們的 API。
