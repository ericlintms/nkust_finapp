import pandas as pd
import numpy as np # Numpy 提供了超級強大的數學與條件判斷小工具

def run_valuation_model():
    # 模擬我們從 Yahoo 抓下來，又經過一點點整理的財報數據
    data = {
        "ticker": ["AAPL", "TSLA", "MSFT", "TRASH.CO"],
        "roe": [0.45, 0.20, 0.38, 0.02],    # ROE 股東權益報酬率
        "pe_ratio": [26.5, 45.0, 35.0, 80], # 本益比
    }
    df = pd.DataFrame(data)
    print("📊 原始資料流進來了：")
    print(df)
    print("\n" + "="*50 + "\n")
    
    # ========================================================
    # 護城河選股演算法 (利用 numpy 的 select 將複雜的業務邏輯程式碼化)
    # ========================================================
    
    # 我們設定多種過濾條件 (Conditions)
    conditions = [
        # 條件 1：價值型好股 (超強護城河 ROE > 15%，且還算便宜的 PE < 30)
        (df['roe'] > 0.15) & (df['pe_ratio'] < 30),
        
        # 條件 2：昂貴垃圾股 (不怎麼賺錢 ROE < 5%，但市場卻炒作它 PE > 50)
        (df['roe'] < 0.05) & (df['pe_ratio'] > 50)
    ]
    
    # 對應著條件，如果中了要貼什麼標籤 (Choices)
    choices = [
        "✅ 被低估價值股", 
        "🚨 昂貴妖股"
    ]
    
    # 使用 np.select，這就是 AI 最愛也是最高效的「向量化打標」方式！
    # 第一個參數放條件，第二個參數放選項，default 表示萬一都沒中，就放最後一個字
    df['value_label'] = np.select(conditions, choices, default="👌 合理區間/一般")
    
    print("📈 分析眼引擎啟動完畢！我們給每檔股票打好標籤了：")
    print(df)
    print("\n最後，我們就可以把這張表寫進資料庫，準備讓 Web 前端來抓囉！")

if __name__ == "__main__":
    run_valuation_model()
