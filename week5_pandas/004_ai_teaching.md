# 與 AI 協作：Pandas 煉金術 (Week 5)

Pandas 是資料科學界最強的工具，但它也有一個缺點：**它的語法超像外星文，極難背誦**。
比如，當我們想要把兩個資料表合併，到底是該用 `merge`, `join` 還是 `concat`？參數是不是 `left_on`, `how='inner'`？

好消息是：**所有 AI 對於寫 Pandas 幾乎都是滿分！**
因為網路上隨處可見 Pandas 的教學，AI 把這些吃得透透的。我們這週最重要的事情，就是學會不要自己寫，**全靠動嘴巴請 AI 寫 Pandas**。

## 💡 AI 提示詞 (Prompt) 技巧分享

當要求 AI 寫資料處理邏輯時，最重要的就是具體描述你手上目前的 **「長相 (Input)」** 跟你想要的 **「結果 (Output)」**。

### ✅ 好的 Prompt 範例

> **你現在是一個資料分析師。**
> 我目前有一個 Pandas DataFrame `df`，裡面存有台股的資料。
>
> **目前的欄位有：**
>
> - `ticker`: 股票代號 (字串)
> - `pe_ratio`: 本益比 (浮點數，可能有 NaN)
> - `roe`: 股東權益報酬率 (浮點數，例如 0.15 代表 15%)
> - `price`: 當前股價
>
> **我需要你幫我進行以下兩步操作：**
>
> 1. 請幫我清除掉任何 `pe_ratio` 或 `roe` 是空值 (NaN) 的那一列。
> 2. 請幫我新增一個欄位叫做 `value_label` (字串)。邏輯如下：
>    - 如果 `roe` > 0.15 且 `pe_ratio` < 15，標籤為 "被低估價值股" (Undervalued)
>    - 如果 `roe` < 0.05 且 `pe_ratio` > 30，標籤為 "昂貴垃圾股" (Overvalued)
>    - 其餘的皆標籤為 "合理/一般" (Fair)
>
> 要求：
>
> - 請使用 Pandas 推薦的向量化寫法（例如 `np.where` 或 `pd.Series.mask`），**絕對不要**叫我寫 `for` 迴圈去跑每一行 (Iterrows)。
> - 給我一段可以直接跑、簡單明瞭的 Python 程式碼。

### 🚨 常見的 AI 翻車踩坑點

1. **AI 常常會愛用 `iterrows` 或 `apply`**：
   有時候 AI 一偷懶，會寫出類似 `df.apply(lambda row: xxx)` 的語法。雖然這跑得動，但完全喪失了 Pandas 最自豪的「向量化極速運算」優勢。遇到這點要勇敢反駁 AI：「請幫我改成向量化的寫法，不要用 apply」。

2. **SettingWithCopyWarning (紅字警告轟炸)**：
   這是 Pandas 新手最常看到的噩夢！當你先篩選了一個副表，又想去修改這個副表的欄位時，Python 就會跳滿整個畫面的警告。
   **防禦機制**：如果你在編輯器看到滿版紅字，馬上把紅字複製貼給 AI，大喊：「遇到 SettingWithCopyWarning 了，請幫我加上 `.copy()` 處理好這個問題！」AI 馬上就會幫你修復了。
