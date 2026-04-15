from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def show_awesome_chart(request: Request):
    
    # 模擬從 yfinance 抓回來的歷史資料 (例如最近 14 天)
    # 為了畫出 Chart.js，最理想的資料結構是把它拆成兩個 List！
    
    # 1. 這是 X 軸的標籤 (時間)
    dates = [
        "10/1", "10/2", "10/3", "10/4", "10/5", 
        "10/8", "10/9", "10/10", "10/11", "10/12",
        "10/15", "10/16", "10/17", "10/18"
    ]
    
    # 2. 這是 Y 軸的資料點 (股價) - 我們模擬一檔一開始盤整，後面大漲的黑馬股
    prices = [
        120, 119, 121, 118, 122, 
        125, 130, 135, 134, 140, 
        145, 150, 148, 155
    ]
    
    # (選修) 這是另一個 Y 軸的資料點 (成交量)
    volumes = [
        1000, 1100, 950, 1200, 1800,
        3500, 4800, 5500, 3100, 6000,
        7200, 8000, 4500, 9100
    ]
    
    # 使用我們前一週學的 Jinja2 傳遞，把這兩個 List 送給網頁端！
    return templates.TemplateResponse(
        request=request, 
        name="w701_chart.html", 
        context={
            "app_title": "動態技術分析",
            "stock_symbol": "飆王科技 (9999.TW)",
            "chart_dates": dates,  # 把時間 List 傳進去
            "chart_prices": prices, # 把股價 List 傳進去
            "chart_volumes": volumes # 給想要挑戰作業的同學參考
        }
    )
