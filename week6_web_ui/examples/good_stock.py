from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
TEMPLATE_DIR = BASE_DIR / "templates"
WEEK5_FILTER_PATH = PROJECT_ROOT / "week5_pandas" / "examples" / "stock_filter.py"

app = FastAPI(title="強弱勢股票觀測站")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def load_week5_stock_filter_module():
    spec = spec_from_file_location("week5_stock_filter", WEEK5_FILTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("無法載入 week5 的 stock_filter.py")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def load_price_data():
    stock_filter = load_week5_stock_filter_module()
    return stock_filter.load_filtered_ohlc().reset_index()


def build_strength_tables(days: int, limit: int) -> dict:
    df = load_price_data().copy()
    df["TradeDate"] = df["TradeDate"].astype("datetime64[ns]")
    df = df.sort_values(["StockId", "TradeDate"])

    grouped_close = df.groupby("StockId")["Close"]
    df["base_close"] = grouped_close.shift(days)
    df["return_pct"] = ((df["Close"] / df["base_close"]) - 1) * 100

    latest_snapshot = (
        df.dropna(subset=["base_close", "return_pct"])
        .loc[lambda frame: (frame["base_close"] > 0) & (frame["Close"] > 0)]
        .groupby("StockId", as_index=False)
        .tail(1)
        .copy()
    )

    latest_snapshot["StockId"] = latest_snapshot["StockId"].astype(str)
    latest_snapshot["days"] = days
    latest_snapshot["trade_date_label"] = latest_snapshot["TradeDate"].dt.strftime("%Y-%m-%d")
    latest_snapshot["return_pct"] = latest_snapshot["return_pct"].round(2)
    latest_snapshot["Close"] = latest_snapshot["Close"].round(2)
    latest_snapshot["base_close"] = latest_snapshot["base_close"].round(2)
    latest_snapshot["StockName"] = ""

    strong_frame = latest_snapshot.sort_values("return_pct", ascending=False).head(limit).copy()
    weak_frame = latest_snapshot.sort_values("return_pct", ascending=True).head(limit).copy()

    strong_stocks = strong_frame.to_dict("records")
    weak_stocks = weak_frame.to_dict("records")

    summary = {
        "universe_count": int(latest_snapshot["StockId"].nunique()),
        "market_date": latest_snapshot["TradeDate"].max().strftime("%Y-%m-%d") if not latest_snapshot.empty else "無資料",
        "avg_return": round(float(latest_snapshot["return_pct"].mean()), 2) if not latest_snapshot.empty else 0.0,
        "positive_count": int((latest_snapshot["return_pct"] > 0).sum()),
        "negative_count": int((latest_snapshot["return_pct"] < 0).sum()),
    }

    return {
        "strong_stocks": strong_stocks,
        "weak_stocks": weak_stocks,
        "summary": summary,
    }


@app.get("/", response_class=HTMLResponse)
async def show_good_stock_dashboard(
    request: Request,
    days: int = Query(default=20, ge=1, le=120, description="最近幾個交易日"),
    limit: int = Query(default=10, ge=3, le=30, description="每區塊顯示幾檔"),
):
    rankings = build_strength_tables(days=days, limit=limit)

    return templates.TemplateResponse(
        request=request,
        name="good_stock.html",
        context={
            "app_title": "強弱勢股票觀測站",
            "days": days,
            "limit": limit,
            **rankings,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)