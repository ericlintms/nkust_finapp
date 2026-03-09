import yfinance as yf
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

# ==========================================
# 基礎建設：資料庫設定 (同 Week 3)
# ==========================================
class StockData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True)
    price: Optional[float] = None
    pe_ratio: Optional[float] = None

sqlite_url = "sqlite:///real_world.db"
# 為了避免畫面太亂，我們這次不開 echo=True
engine = create_engine(sqlite_url)
SQLModel.metadata.create_all(engine)

# ==========================================
# 第一步：Extract & Transform (抓取並清理)
# ==========================================
def extract_and_transform(ticker_list: list) -> list:
    clean_data = []
    
    for tk in ticker_list:
        print(f"🔍 處理中: {tk}")
        try:
            stock = yf.Ticker(tk)
            info = stock.info
            price = info.get("currentPrice") or info.get("previousClose")
            pe = info.get("trailingPE")
            
            # 如果連價錢都抓不到，這筆資料沒意義，我們就過濾掉它 (Transform 邏輯)
            if price is None:
                print(f"⚠️ {tk} 找不到股價，略過不處理。")
                continue
                
            clean_data.append({
                "ticker": tk,
                "price": price,
                "pe_ratio": pe
            })
            
        except Exception as e:
            print(f"❌ 發生錯誤 {tk}: {str(e)}")
            continue # 確保迴圈能夠繼續下一檔，不要崩潰
            
    return clean_data

# ==========================================
# 第二步：Load (載入資料庫)
# ==========================================
def load_to_database(data_list: list):
    print("📦 準備將資料寫入 SQLite (real_world.db)...")
    
    with Session(engine) as session:
        for item in data_list:
            # 這裡我們展示一個比較進階的邏輯「Upsert」(如果存在就更新，不存在就新增)
            
            # 先去 DB 裡找找看這檔股票是不是已經在裡面了
            statement = select(StockData).where(StockData.ticker == item["ticker"])
            existing_stock = session.exec(statement).first()
            
            if existing_stock:
                # 已經有了！那我們就更新它的價格跟 PE 即可
                existing_stock.price = item["price"]
                existing_stock.pe_ratio = item["pe_ratio"]
                session.add(existing_stock)
                print(f"🔄 更新現有資料：{item['ticker']}")
            else:
                # 找不到，表示是全新的一檔股票！直接新增
                new_stock = StockData(
                    ticker=item["ticker"],
                    price=item["price"],
                    pe_ratio=item["pe_ratio"]
                )
                session.add(new_stock)
                print(f"🆕 新增全新資料：{item['ticker']}")
                
        # 全部裝進推車後，一次結帳！
        session.commit()
    print("✅ 寫入完成！")

if __name__ == "__main__":
    # 我們設定一份想要觀察的股票清單
    my_watch_list = ["2330.TW", "2454.TW", "2317.TW", "MSFT"]
    
    # 開始 ETL 生產線！
    print("=== 🚀 ETL 生產線啟動 ===")
    
    # 1. E & T
    scraped_data = extract_and_transform(my_watch_list)
    
    # 2. L
    if scraped_data:
        load_to_database(scraped_data)
        
    print("=== 🎉 任務圓滿結束 ===")
