# 與 AI 協作：資料庫設計篇 (Week 3)

這週我們要學習怎麼利用 Vibe Coding 讓 AI 幫我們生出資料庫的結構。

設計資料庫結構，通常是軟體工程裡比較需要經驗的部分。如果關聯設計得不好，後面的程式會寫得極度痛苦。好險，我們有 AI 可以幫我們打底！

## 💡 AI 提示詞 (Prompt) 技巧分享

當我們想要建立新的資料表 (Table) 時，千萬不要直接跟 AI 說：「幫我寫一個 SQLModel」。
我們要像是在使喚專業的架構師一樣，把我們的**業務邏輯** (我們到底想記錄什麼) 交代清楚：

### ✅ 好的 Prompt 範例

> **你現在是一個資深的 FinTech 後端工程師。**
> 我正在開發一個股票分析系統，後端使用 Python 的 FastAPI 與 **SQLModel**。
>
> 請幫我設計一個資料表來儲存「台股每日的基本面數據」。
>
> 我需要以下欄位：
>
> 1. id (主鍵)
> 2. ticker (股票代號，例如 "2330.TW")
> 3. date (資料日期)
> 4. close_price (收盤價)
> 5. pe_ratio (本益比)
> 6. roe (股東權益報酬率)
>
> 要求：
>
> - 請使用 `SQLModel` 並標記 `table=True`。
> - `ticker` 與 `date` 常常會拿來當作查詢條件，請幫我加上 Index。
> - 欄位請加上清楚的中文註解。
> - 除了定義 Model 之外，請順便寫一個可以自動建立 SQLite `.db` 檔案並生成 Table 的 `create_db_and_tables()` 函數。

### 🚨 常見的 AI 翻車踩坑點

在使用 AI 生成資料庫程式碼時，請務必幫我緊盯這幾件事：

1. **忘記 `table=True`**：
   SQLModel 的 class 必須要有 `class Stock(SQLModel, table=True):`。如果 AI 忘記加 `table=True`，這個 class 就只是一個普通的 Pydantic 驗證模型，**不會**在資料庫裡建出一張表！這是新手最常遇到的鬼打牆。

2. **主鍵設定錯誤**：
   記得檢查主鍵 ID 是不是這樣寫：`id: Optional[int] = Field(default=None, primary_key=True)`。必須要接受 `None`，因為一開始我們在 Python 建立物件時，還沒存進資料庫，它還沒有被分配流水號 ID。

3. **Session 忘了 Commit**：
   當你叫 AI 寫 CRUD 的範例碼時，有時候它會做了 `session.add(...)` 但忘記寫 `session.commit()`。沒有 commit 的話，資料只存在記憶體裡，一關掉程式就不見了！

把這三點印在腦海裡，你在審查 AI 的程式碼時就會像個大師。
