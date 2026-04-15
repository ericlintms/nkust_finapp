from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def show_dashboard(request: Request):
    
    # 模擬從 Week 5 的 Pandas 運算完，或是從資料庫裡面撈出來的一大串字典清單
    mock_stock_list = [
        {"ticker": "2330.TW", "name": "台積電", "price": 820.5, "pe": 20.3, "status": "合理"},
        {"ticker": "2454.TW", "name": "聯發科", "price": 1050.0, "pe": 16.5, "status": "超值"},
        {"ticker": "AAPL", "name": "蘋果", "price": 170.2, "pe": 26.1, "status": "昂貴"},
        {"ticker": "2317.TW", "name": "鴻海", "price": 155.0, "pe": 14.5, "status": "超值"}
    ]
    
    # 計算一下總共有幾檔股票 (要顯示在 Dashboard 卡片上的數據)
    total_count = len(mock_stock_list)
    
    # 把它們一起丟給 HTML 模板！
    return templates.TemplateResponse(
        request=request, 
        name="w602_dashboard.html", 
        context={
            "app_title": "護城河投資儀",
            "stocks": mock_stock_list,
            "count": total_count
        }
    )
