import yfinance as yf

def fetch_single_stock_info(ticker_symbol: str):
    print(f"📡 正在前往 Yahoo Finance 尋找 {ticker_symbol} 的資料...")
    
    # 建立一個 yfinance 的 Ticker 物件 (就像跟 Yahoo 指定我們關注哪檔股票)
    stock = yf.Ticker(ticker_symbol)
    
    try:
        # .info 是一個超級大的 Dictionary，裡面包含了這家公司幾乎所有的基本面資料
        info = stock.info
        
        # 我們只挑出我們需要的欄位！這裡就是 ETL 裡面的「Transform (轉換與過濾)」
        
        # 取得最新收盤價。有些欄位在盤中叫做 currentPrice，盤後可能叫 previousClose
        price = info.get("currentPrice") or info.get("previousClose")
        
        # 取得本益比 (Trailing PE 是採用過去一年的獲利算出的本益比)
        pe_ratio = info.get("trailingPE")
        
        # 取得公司名稱 (給我們自己看開心的)
        name = info.get("shortName", "未知名稱")
        
        print(f"✅ 成功抓取！")
        print(f"  - 公司: {name}")
        print(f"  - 價格: ${price}")
        print(f"  - 本益比: {pe_ratio}")
        
        return {
            "ticker": ticker_symbol,
            "price": price,
            "pe_ratio": pe_ratio
        }

    except Exception as e:
        print(f"❌ 抓取資料失敗！原因：{str(e)}")
        return None

if __name__ == "__main__":
    # 測試台積電
    fetch_single_stock_info("2330.TW")
    print("-" * 30)
    # 測試蘋果
    fetch_single_stock_info("AAPL")
