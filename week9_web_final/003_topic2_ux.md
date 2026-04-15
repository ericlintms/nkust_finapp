# 主題二：使用者體驗與錯誤處理 (UX & Error Handling)

在真實世界裡，軟體有 50% 的程式碼都是用來處理「意外的」。
使用者會亂輸入文字、手機會突然斷網、Yahoo Finance 有時候會封鎖你的 IP...。如果遇到這些事情，我們的程式如果只會顯示 `Internal Server Error (500)`，這就是一個不及格的 App！

## 1. 畫面上的防呆機制 (Validation)

你還記得 Week 8 的篩選器表單嗎？
```html
<input type="number" name="max_pe" min="0" max="1000">
```
只要在 `<input>` 加上 `min="0"`，就能強制規定使用者不能輸入負數的本益比。這種在第一線就把愚蠢錯誤擋下來的機制，在業界叫做「前端驗證」。

## 2. 優雅的失敗 (Graceful Degradation)

如果我們今天在後端 (FastAPI) 要去抓資料，結果不巧網路斷線了怎麼辦？千萬不要讓整個系統崩潰！

```python
@app.get("/update_data")
async def update_stock():
    try:
        # 嘗試去網路抓資料...
        new_data = fetch_yfinance_data()
        return {"status": "更新成功！"}
    except Exception as e:
        # 萬一失敗了，生氣摔東西是沒用的，我們要溫柔的告訴前端：
        # 「目前無法取得最新資料，但您可以先看昨天存回來的舊資料喔！」
        # 回傳一個友善的 JSON，讓前端網頁能跳出優雅的警告框。
        return {"status": "error", "message": "Yahoo 伺服器打瞌睡了，請稍後再試！"}
```

## 3. 安撫等待的心：Loading 狀態

爬蟲去抓 100 檔股票的資料可能需要 5 秒鐘。在這個網路時代，如果網頁卡住 2 秒沒反應，使用者就會瘋狂連按重新整理 (這會讓伺服器更當！)。

**好做法：**
當使用者按下「開始篩選」按鈕時，可以用 JavaScript 偷偷把按鈕變成灰色的，並且把文字換成帶有旋轉動畫的圖示：
`<button disabled> ⏳ 計算海量數據中... 請稍候</button>`

以上這三點，就是決定這是一個「大學生交差的期末作業」還是一個「具備商業價值的好產品」的關鍵分水嶺！
