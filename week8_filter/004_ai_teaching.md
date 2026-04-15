# 與 AI 協作：篩選器整合篇 (Week 8)

在實作雙向互動的表單時，程式會牽涉到 **前端 HTML (`<form>`)** 與 **後端 Python (FastAPI 接收)**，許多初學者會在這個跨界整合的階段卡關，常常出現傳出的資料不符或是抓不到變數的錯誤。好在只要向 AI 指令夠精確，這些都只是小菜一碟。

## 💡 AI 提示詞 (Prompt) 技巧分享

當要求 AI 幫你寫這種同時牽涉前後端的程式時，你**必須強制規定它使用相同的變數名稱**。

### ✅ 好的 Prompt 範例

> **你現在是一個全端工程師 (Full-Stack Developer)。**
> 我的系統使用 **FastAPI**, **Pandas**, 和 **Jinja2 (搭配 Bootstrap 5)**。
> 
> 請幫我實作一個「股票條件篩選器 (Stock Screener)」。我需要兩塊程式碼：
> 
> **第一塊：網頁前端 (HTML 表單)**
> - 需要一個搜尋表單。裡面有兩個條件：
>    1. 收盤價 `max_price` (輸入類型為 Number)
>    2. 本益比上限 `pe_limit` (輸入類型為 Number)
> - 請使用 GET 方法將表單送到 `/screener_results`。
> - 表單外觀請用 Bootstrap 稍微排版 (例如放進一排 `row` 裡)。
> 
> **第二塊：後端 (FastAPI Python)**
> - 請寫一個對應的 `/screener_results` GET 端點。
> - 請接住剛才 HTML 指定的 `max_price` 與 `pe_limit` 這兩個參數 (請將它們設定為 Optional 允許空白)。
> - 假設我有一個現成的 Pandas DataFrame 叫做 `all_stocks_df`，請示範如何用這兩個參數將表格過濾。如果使用者沒填寫某個條件，就不要對那個欄位進行過濾。
> - 最後請將結果轉成字典 list (`df.to_dict('records')`) 模擬回傳給 Jinja2。
> 
> 請不要給我零散的片段，請將這兩個部分完整寫出，並加上清楚的註解。

### 🚨 常見的 AI 翻車踩坑點

1. **命名對不上 (致命傷！)**：
   有時候 AI 前端 HTML 的 `name="pe_ratio_max"`，但到了 Python 那邊，它用另外的變數去接 `async def xxxx(max_pe: float)`。因為名字對不起來，Python 會跟你抱怨這包公文夾裡根本沒有它要的東西，直接當機。
   **解決方法**：拿到這兩包 code 時，第一時間像個驗票員一樣檢查兩邊的名字。

2. **型別錯誤的問題 (Type Hinting)**：
   從網址後面 (`?max_price=100.5`) 傳過來的東西，本質上都是一串字串 (String)。如果你在 Python 參數沒有標示出 `max_price: float`，有些時候 Pandas 拿字串去跟數字比大小 (`"100" < 50`) 就會導致程式大崩潰。AI 為了省字有時會漏寫。
   **防禦措施**：記得強制加上 `float` 或 `int` 的標記，讓 FastAPI 在收件時直接先幫你做型別轉換。

3. **使用者甚麼都沒填就送出** (空值災難)：
   如果對方沒輸入數字直接按 Enter 鍵，會傳送 `?max_price=` (一個空字串)。如果你沒請 AI 加上「防呆檢查 (例如如果是 None 就不處理)」，你的 Pandas 篩選條件就會報錯。
