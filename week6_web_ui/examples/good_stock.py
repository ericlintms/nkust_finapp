import argparse
import sqlite3
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

try:
    from .auth_utils import (
        JWT_COOKIE_NAME,
        JWT_EXPIRE_SECONDS,
        AuthError,
        authenticate_user,
        create_jwt,
        decode_jwt,
        init_auth_db,
    )
except ImportError:
    from auth_utils import (
        JWT_COOKIE_NAME,
        JWT_EXPIRE_SECONDS,
        AuthError,
        authenticate_user,
        create_jwt,
        decode_jwt,
        init_auth_db,
    )


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
LOCAL_DB_PATH = BASE_DIR / "crawldata.sqlite3"
PROJECT_DB_PATH = BASE_DIR.parents[1] / "crawldata.sqlite3"

app = FastAPI(
    title="強弱勢股票觀測站",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
PUBLIC_PATHS = {"/login"}

# 啟動時先確保 auth.db 存在，這樣老師只要建立使用者後即可直接示範登入流程。
init_auth_db()


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

    latest_market_date = max((item["trade_date"] for item in latest_snapshot), default=None)
    strong_stocks = sorted(latest_snapshot, key=lambda item: item["return_pct"], reverse=True)[:limit]
    weak_stocks = sorted(latest_snapshot, key=lambda item: item["return_pct"])[:limit]

    # trade_date 只用來做伺服器端統計，不需要直接送進 HTML 或 JSON，
    # 所以回傳前把它移除，避免之後 API 序列化 datetime 時踩到型別問題。
    def serialize_stock(item: dict) -> dict:
        return {key: value for key, value in item.items() if key != "trade_date"}

    summary = {
        "universe_count": len(latest_snapshot),
        "market_date": latest_market_date.strftime("%Y-%m-%d") if latest_market_date else "無資料",
        "avg_return": round(
            sum(item["return_pct"] for item in latest_snapshot) / len(latest_snapshot),
            2,
        ) if latest_snapshot else 0.0,
        "positive_count": sum(1 for item in latest_snapshot if item["return_pct"] > 0),
        "negative_count": sum(1 for item in latest_snapshot if item["return_pct"] < 0),
    }

    return {
        "strong_stocks": [serialize_stock(item) for item in strong_stocks],
        "weak_stocks": [serialize_stock(item) for item in weak_stocks],
        "summary": summary,
    }


def read_token_from_request(request: Request) -> str | None:
    """
    瀏覽器示範時主要從 HttpOnly cookie 取 JWT；
    若學生想用 Postman 或 curl 打 API，也可以改走 Authorization: Bearer。
    """
    authorization = request.headers.get("authorization", "")
    if authorization.startswith("Bearer "):
        return authorization.removeprefix("Bearer ").strip()

    return request.cookies.get(JWT_COOKIE_NAME)


def build_unauthorized_response(request: Request, detail: str):
    """HTML 頁面導回登入頁；API 則回傳 401 JSON，兩種情境的 UX 會比較自然。"""
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=401, content={"detail": detail})

    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(JWT_COOKIE_NAME)
    return response


@app.middleware("http")
async def require_jwt_for_private_pages(request: Request, call_next):
    """
    除了 /login 之外，所有頁面與 API 都必須先通過 JWT 驗證。

    這裡使用 middleware 的原因是：
    1. 規則集中，學生可以清楚看到「哪些路徑是公開、哪些需要登入」
    2. 不必每支 route 都重複貼一段驗證程式
    3. 可以依請求型態決定要 redirect 還是回 401 JSON
    """
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    token = read_token_from_request(request)
    if not token:
        return build_unauthorized_response(request, "缺少登入 token")

    try:
        claims = decode_jwt(token)
    except AuthError as exc:
        return build_unauthorized_response(request, str(exc))

    request.state.userid = claims["sub"]
    request.state.jwt_claims = claims
    return await call_next(request)


@app.get("/login", response_class=HTMLResponse)
async def show_login_page(request: Request):
    """
    獨立登入頁只有帳號與密碼欄位，不提供註冊功能，
    符合示範系統預先建立帳號的需求。
    """
    token = read_token_from_request(request)
    if token:
        try:
            decode_jwt(token)
        except AuthError:
            pass
        else:
            return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "app_title": "強弱勢股票觀測站",
            "error_message": None,
            "userid": "",
        },
    )


@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    userid: str = Form(...),
    passwd: str = Form(...),
):
    user = authenticate_user(userid=userid, password=passwd)
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            status_code=401,
            context={
                "app_title": "強弱勢股票觀測站",
                "error_message": "帳號或密碼錯誤，請重新輸入。",
                "userid": userid,
            },
        )

    token = create_jwt(userid=user["userid"])
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        max_age=JWT_EXPIRE_SECONDS,
        httponly=True,
        samesite="lax",
    )
    return response


@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(JWT_COOKIE_NAME)
    return response


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
            "current_user": request.state.userid,
            "days": days,
            "limit": limit,
            **rankings,
        },
    )


@app.get("/api/rankings")
async def get_rankings_api(
    request: Request,
    days: int = Query(default=20, ge=1, le=120, description="最近幾個交易日"),
    limit: int = Query(default=10, ge=3, le=30, description="每區塊顯示幾檔"),
):
    """
    這支 API 是示範「同一顆 JWT 可以保護 HTML 頁面，也可以保護 JSON API」。
    若沒有 token，middleware 會先擋下來，不會執行到這裡。
    """
    return {
        "user": request.state.userid,
        "days": days,
        "limit": limit,
        **build_strength_tables(days=days, limit=limit),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="強弱勢股票觀測站")
    parser.add_argument("--host", default="127.0.0.1", help="要綁定的主機位址")
    parser.add_argument("--port", type=int, default=8000, help="要監聽的連接埠")
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
