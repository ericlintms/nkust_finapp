from sqlmodel import Session, select
from w301_create_db import Stock, engine, create_db_and_tables

# 先確保資料庫裡面真的有表格存在
create_db_and_tables()

print("\n--- 等等下面的輸出將示範 CRUD 的四大操作 ---\n")

def perform_crud_operations():
    # 使用 Session (建立一個連線的工作階段)
    # 使用 with 語句的好處是，運作完這層縮排後，Python 會幫我們自動安全地關掉連線
    with Session(engine) as session:
        
        # ==========================================
        # 1. Create (新增資料)
        # ==========================================
        print("\n[Create] 正在新增一筆股票資料...")
        
        # 建立一個 Python 物件
        tsmc = Stock(ticker="2330.TW", price=800.0, pe_ratio=20.5)
        
        # 把它放進推車 (Session) 裡
        session.add(tsmc)
        
        # 結帳！正式寫入資料庫！
        session.commit()
        
        # 若想看寫入後產生的流水號 ID，我們必須要從資料庫 refresh (重新讀取) 它一次
        session.refresh(tsmc)
        print(f"✅ 新增成功！台積電現在在資料庫裡的 id 號碼是：{tsmc.id}")

        # ==========================================
        # 2. Read (讀取資料)
        # ==========================================
        print("\n[Read] 正在查詢資料庫裡所有的股票資料...")
        
        # 寫一個查詢的草稿：幫我選出 (select) 所有的 Stock
        statement = select(Stock)
        
        # 請 session 送出查詢，並把拿到結果轉換成清單 (all())
        results = session.exec(statement).all()
        
        print(f"📖 資料庫裡現在總共有 {len(results)} 檔股票。清單如下：")
        for stock in results:
            print(f"   - {stock.ticker}: 價格 ${stock.price}, PE = {stock.pe_ratio}")

        # 如果只想抓某一檔股票怎麼辦？
        # 加條件 (where)！
        specific_stock_statement = select(Stock).where(Stock.ticker == "2330.TW")
        found_stock = session.exec(specific_stock_statement).first() # 取第一筆符合的
        print(f"🔍 針對搜尋結果: 找到 {found_stock.ticker}")

        # ==========================================
        # 3. Update (更新資料)
        # ==========================================
        print("\n[Update] 假設今天大漲！我們要更新台積電價格...")
        
        if found_stock:
            # 直接把物件的屬性改掉
            found_stock.price = 820.0
            found_stock.pe_ratio = 21.0
            
            # 放回推車準備結帳
            session.add(found_stock)
            
            # 結帳！
            session.commit()
            print("📈 價格更新成功！")
            
            # 再讀出來看看是不是真的改了
            session.refresh(found_stock)
            print(f"   更新後的價格確認：{found_stock.price}")

        # ==========================================
        # 4. Delete (刪除資料) - 選修操作，實務上比較少真刪除
        # ==========================================
        print("\n[Delete] 示範如何刪除資料...")
        
        # 給我很果斷的刪除下去 (把物件交給 delete 指令)
        # session.delete(found_stock)
        
        # 記得要結帳刪除的動作才會生效
        # session.commit()
        # print("🗑️ 資料已刪除！")
        
        print("⚠️ 為了讓大家等等可以重複練習，我先把刪除的程式碼註解起來了，你可以自己打開玩看看喔！")

if __name__ == "__main__":
    perform_crud_operations()
