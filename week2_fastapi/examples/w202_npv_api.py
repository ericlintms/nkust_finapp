from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import List
from pathlib import Path

app = FastAPI(title="現金流計算 API")

# 設定 Jinja2 模板路徑
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

def calculate_npv(rate: float, cash_flows: List[float]) -> float:
    npv = 0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + rate) ** t)
    return npv

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """回傳首頁"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/calculate/npv")
def get_npv(rate: float, cash_flows_str: str):
    """
    計算 NPV 值的 API \n
    :param rate: 折現率 (例如 0.05) \n
    :param cash_flows_str: 現金流字串以逗號分隔，例如 '-10000,3000,4200,6800'
    """
    try:
        # 將字串分割並轉換為浮點數 List
        cash_flows = [float(cf.strip()) for cf in cash_flows_str.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="現金流格式錯誤，請確保以逗號分隔數字")
    
    result = calculate_npv(rate, cash_flows)
    
    return {
        "rate": rate,
        "cash_flows": cash_flows,
        "npv_value": round(result, 2),
        "is_good_investment": result > 0
    }

# 啟動方式:
# uvicorn 02_npv_api:app --reload
