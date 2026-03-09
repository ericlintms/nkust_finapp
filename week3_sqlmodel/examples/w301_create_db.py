from sqlmodel import SQLModel, Field, create_engine
from typing import Optional

# 1. 定義資料表模型 (Data Model)
# 記得一定要加上 table=True，SQLModel 才知道這是一個要存進資料庫的資料表
class Stock(SQLModel, table=True):
    # id 設定為 Optional[int]，並設定為主鍵。這樣資料庫會自動幫我們產生 1, 2, 3 的流水編號。
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 股票代號，必填字串，設定 index=True 讓未來用代號搜尋時速度飛快。
    ticker: str = Field(index=True)
    
    # 股價，允許為空 (Optional)，因為有時候抓不到最新價格
    price: Optional[float] = None
    
    # 本益比，同樣允許為空
    pe_ratio: Optional[float] = None

# 2. 準備連線到資料庫
# 我們告訴系統要建立一個 SQLite 資料庫，檔名叫做 database.db
# echo=True 是用來學習的祕技！它會把背後產生的所有 SQL 語言都印在畫面上給你看！
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Engine 是所有資料庫操作的引擎 (核心設備)
engine = create_engine(sqlite_url, echo=True)

# 3. 執行建立資料表的魔法
def create_db_and_tables():
    print("🚀 準備開始建立資料庫與資料表...")
    
    # 這是最神奇的一行程式碼。
    # SQLModel 會去尋找所有寫了 table=True 的 Class (這裡就是 Stock)，然後在資料庫裡建好對應的結構。
    SQLModel.metadata.create_all(engine)
    
    print("✅ 資料表建立完成！去看看資料夾有沒有多出一個 database.db 檔案吧！")

if __name__ == "__main__":
    # 只有當直接執行這個檔案時，才會出發這個函數
    create_db_and_tables()
