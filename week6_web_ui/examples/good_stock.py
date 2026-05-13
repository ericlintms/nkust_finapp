import argparse
import sqlite3
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
LOCAL_DB_PATH = BASE_DIR / "crawldata.sqlite3"
PROJECT_DB_PATH = BASE_DIR.parents[1] / "crawldata.sqlite3"

app = FastAPI(title="強弱勢股票觀測站")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def resolve_db_path() -> Path:
    for db_path in (LOCAL_DB_PATH, PROJECT_DB_PATH):
        if db_path.exists():
            return db_path

    raise FileNotFoundError(
        "找不到 crawldata.sqlite3。請先把資料庫放在 good_stock.py 同目錄，"
        "或維持專案根目錄中的 crawldata.sqlite3。"
    )


@lru_cache(maxsize=1)
def load_price_data() -> dict[str, list[dict]]:
    query = """
    SELECT StockId, TradeDate, Close
    FROM OHLC
    WHERE CAST(StockId AS TEXT) GLOB '[0-9][0-9][0-9][0-9]'
    ORDER BY StockId, TradeDate
    """

    with sqlite3.connect(resolve_db_path()) as conn:
        rows = conn.execute(query).fetchall()

    grouped_prices: dict[str, list[dict]] = {}
    for stock_id, trade_date, close in rows:
        grouped_prices.setdefault(str(stock_id), []).append(
            {
                "TradeDate": datetime.strptime(trade_date, "%Y/%m/%d"),
                "Close": float(close),
            }
        )

    return grouped_prices


def build_strength_tables(days: int, limit: int) -> dict:
    latest_snapshot = []

    for stock_id, history in load_price_data().items():
        if len(history) <= days:
            continue

        latest = history[-1]
        base = history[-1 - days]
        if base["Close"] <= 0 or latest["Close"] <= 0:
            continue

        latest_snapshot.append(
            {
                "StockId": stock_id,
                "StockName": "",
                "Close": round(latest["Close"], 2),
                "base_close": round(base["Close"], 2),
                "return_pct": round(((latest["Close"] / base["Close"]) - 1) * 100, 2),
                "trade_date_label": latest["TradeDate"].strftime("%Y-%m-%d"),
                "trade_date": latest["TradeDate"],
            }
        )

    strong_stocks = sorted(latest_snapshot, key=lambda item: item["return_pct"], reverse=True)[:limit]
    weak_stocks = sorted(latest_snapshot, key=lambda item: item["return_pct"])[:limit]

    summary = {
        "universe_count": len(latest_snapshot),
        "market_date": max(item["trade_date"] for item in latest_snapshot).strftime("%Y-%m-%d") if latest_snapshot else "無資料",
        "avg_return": round(
            sum(item["return_pct"] for item in latest_snapshot) / len(latest_snapshot),
            2,
        ) if latest_snapshot else 0.0,
        "positive_count": sum(1 for item in latest_snapshot if item["return_pct"] > 0),
        "negative_count": sum(1 for item in latest_snapshot if item["return_pct"] < 0),
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


def main() -> None:
    parser = argparse.ArgumentParser(description="強弱勢股票觀測站")
    parser.add_argument("--host", default="127.0.0.1", help="要綁定的主機位址")
    parser.add_argument("--port", type=int, default=8000, help="要監聽的連接埠")
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
