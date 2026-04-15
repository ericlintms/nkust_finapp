from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from typing import Optional
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 假設這是我們系統剛開機時，從 SQLite 資料庫或 Yahoo 爬蟲拿回來的原生資料。
# 我們用它來製造一個原始的 Pandas DataFrame 存放在記憶體裡。
mock_data = [
    {"ticker": "2330.TW", "name": "台積電", "price": 820.5, "pe": 20.3},
    {"ticker": "2454.TW", "name": "聯發科", "price": 1050.0, "pe": 16.5},
    {"ticker": "AAPL", "name": "蘋果", "price": 170.2, "pe": 26.1},
    {"ticker": "2317.TW", "name": "鴻海", "price": 155.0, "pe": 14.5},
    {"ticker": "2883.TW", "name": "開發金", "price": 14.2, "pe": 11.2}
]
raw_df = pd.DataFrame(mock_data)


# 建立一個首頁路由，同時兼任接收篩選結果的總部。
# 所以我們要在括號裡面設計好接球手 (max_price 和 max_pe)
@app.get("/")
async def show_screener(
    request: Request,
    max_price: Optional[float] = None, # 允許沒填寫，所以是 Optional
    max_pe: Optional[float] = None
):
    
    # 【超級重要的一步】：先把原始資料拷貝一份出來，不要破壞唯一的底層資料喔！
    filter_df = raw_df.copy()
    
    # ----------------------------------------------------
    # 開始使用 Pandas 進行邏輯過濾！(如果不為 None，代表使用者有輸入)
    # ----------------------------------------------------
    if max_price is not None:
        # 只保留「價格」小於等於使用者輸入條件的股票
        filter_df = filter_df[filter_df["price"] <= max_price]
        
    if max_pe is not None:
        # 繼續過濾，只保留「本益比」小於等於使用者限制的股票
        filter_df = filter_df[filter_df["pe"] <= max_pe]

    # 過濾完畢！把 Pandas 裡面剩下的精華結果，重新轉成 Dictionary List 送出！
    good_stocks_list = filter_df.to_dict('records')

    # 回傳給 Jinja2 去產生結果報表！
    # 我們順便把剛剛使用者輸入的參數也回傳 (為了可以留在輸入框裡不要消失)
    return templates.TemplateResponse(
        request=request, 
        name="w801_screener.html", 
        context={
            "app_title": "嚴謹的大師選股器",
            "stocks": good_stocks_list,  # 這個是過濾過後的結果唷！
            "result_count": len(good_stocks_list),
            # 我們把這些丟回去，讓等一下網頁表單上可以記住輸入過的值
            "saved_max_price": max_price if max_price else "",
            "saved_max_pe": max_pe if max_pe else ""
        }
    )
