# AI 協作指南 (Week 2)

## 1. 遇到 Server Error 怎麼自救？

一開始我們啟動 FastAPI 的時候，最常遇到的挫折就是不小心打錯字或是縮排(空白鍵)對不齊，導致伺服器一啟動就崩潰 (`Internal Server Error` 或終端機噴出一堆紅字)。

- **我們的協作練習**: 學習「如何向 AI 有效求救」。
- **Prompt 示範**: "我在啟動 FastAPI 的時候，終端機出現了以下這段錯誤 `[把整段紅字 Traceback 複製貼上]`。請問這是什麼意思？我該怎麼修復我寫的 `w202_npv_api.py`？"

## 2. 預防 AI 產生「型態幻覺」

AI 在幫我們生 API 程式碼時，有時候會偷懶忘記加上 Python 的型別提示 (Type Hint)。但 FastAPI 其實超級依賴這個提示來幫我們擋掉錯誤的資料！

- **錯誤情況**: AI 可能會給我們這種光禿禿的寫法 `def calculate(rate):`
- **引導 AI 修改**: 我們可以反過來要求 AI：「請幫我在 FastAPI 路由的函式定義裡，補上明確的 Type Hints，例如寫成 `rate: float`。因為我需要用這些型別讓 Swagger UI 自動產生測試選單，而且可以防止不懂的人把 String (字串) 給傳進來。」

## 3. 把錯誤漂亮地丟回去 (HTTPException)

AI 通常比較天真，只會假設「Happy Path」(就是以為每個使用者都會乖乖輸入我們想要的數字)。
但我們財管系的實務模型裡，常常會有人頑皮輸入不合法的字串或是負數。這時候我們要能霸氣地對 AI 說：「如果收到的字串沒辦法被轉換成浮點數陣列 (float list)，請幫我寫個機制捕捉 ValueError 的錯誤，並拋出 `HTTPException(400)` 告訴前端『欸你這是個 Bad Request，回去重寫參數！』」
