# 實務範例與實作 (Week 7)

準備好讓我們的網頁動起來了嗎？這週的範例會讓我們將 Python 和網頁的最後一哩路給徹底打通！

## 系統要怎麼找到網頁檔案？

提醒：一樣我們所有的 HTML 還是要乖乖放在 `templates/` 資料夾底下。

```
week7_chartjs/
├── examples/
│   ├── templates/          
│   │   └── w701_chart.html    <-- 畫布與 JS 藏在這裡
│   └── w701_show_chart.py     <-- 這裡準備歷史股價
```

## 我們的練習清單

### 1. 例題一：動態股價趨勢圖實戰
- **對應檔案**: `examples/w701_show_chart.py` 與 `examples/templates/w701_chart.html`
- **練習目的**: 完整體會一遍 `Python準備陣列` -> `Jinja2把陣列傳給前端` -> `JavaScript收下陣列並透過Chart.js畫圖` 的經典三角戰術！
- **實作任務**:
  1. 切換目錄到 `week7_chartjs/examples/`。
  2. 啟動伺服器：`uvicorn w701_show_chart:app --reload`。
  3. 前往網頁：`http://127.0.0.1:8000/`。
  4. 你應該會看到一張非常現代感、具有滑鼠懸停 (Hover) 動畫的滑順折線圖！它會帶有漸層底色與淡淡的網格。
  5. **魔法測試**：試著把滑鼠浮在任何一個轉折點上方，是不是會跳出那天的日期與價格？

### 2. 進階挑戰 (給行有餘力的你)：雙軸大師
試著跟你的 AI 合作！把剛才我們 `w701_show_chart.py` 裡面多準備好的 `volume_list` (成交量)，一起傳進網頁裡面。
試著請 AI 在同一張 Chart.js 的畫布上，加上第二個資料集，用「直條圖 (Bar Chart)」來表現成交量！
這可是專業看盤軟體 (如 TradingView) 的基礎技能呢！
