import pandas as pd

def demonstrate_pandas():
    # 這是傳統的 Python 字典組成的 List (你可以想像這是資料庫剛吐出來的樣子)
    raw_data = [
        {"ticker": "2330.TW", "price": 820, "eps": 40},
        {"ticker": "2454.TW", "price": 1050, "eps": 60},
        {"ticker": "2317.TW", "price": 150, "eps": 10},
        {"ticker": "NG_STOCK", "price": 20, "eps": -2}, # EPS 為負的公司
    ]
    
    # 魔法第一課：變身！將原生格式轉成 DataFrame
    df = pd.DataFrame(raw_data)
    
    print("📋 1. 原始的資料表長這樣：")
    print(df)
    print("-" * 40)
    
    # 魔法第二課：計算本益比 (Price / EPS)
    print("🧮 2. 一秒鐘算出所有的 PE 本益比：")
    # 瞬間就把所有的價格除以獲利，並塞進新的欄位 'pe_ratio'
    df['pe_ratio'] = df['price'] / df['eps']
    print(df)
    print("-" * 40)
    
    # 魔法第三課：極速篩選 (Filter)
    print("🔍 3. 我只要找賺錢的公司 (EPS > 0)，且本益比小於 25 的股票：")
    
    # Pandas 裡的 AND 條件要用 `&`，且每個條件要用括號包起來！
    good_stocks_df = df[(df['eps'] > 0) & (df['pe_ratio'] < 25)]
    print(good_stocks_df)
    print("-" * 40)

if __name__ == "__main__":
    demonstrate_pandas()
