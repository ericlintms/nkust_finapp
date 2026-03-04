# 請先安裝: pip install fastapi uvicorn
from fastapi import FastAPI

# 初始化 FastAPI 應用程式
app = FastAPI(title="FinApp 基礎課程 API")

# 使用裝飾器定義路由與 HTTP 方法
@app.get("/")
def read_root():
    return {"message": "Hello, 歡迎來到財經 App 實作課程！"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}, 準備好學 FastAPI 了嗎？"}

# 啟動方式:
# 在終端機輸入: uvicorn 01_hello_api:app --reload
# 然後用瀏覽器開啟 HTTP://127.0.0.1:8000/docs 查看 Swagger UI
