from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

# 關鍵設定：告訴 FastAPI 去哪裡找我們的 HTML 模板檔案
# 注意：這裡的 "templates" 代表它會往這支 Python 程式同級目錄下的 templates 資料夾找
templates = Jinja2Templates(directory="templates")

# 設定一個包含路由參數 {user_name} 的網址
@app.get("/hello/{user_name}")
async def read_hello_page(request: Request, user_name: str):
    
    # 在真實世界裡，我們可以在這裡寫複雜的運算：從資料庫撈出使用者的餘額算利息等
    interest = 1500
    
    # 重點來了！
    # return templates.TemplateResponse 負責把資料跟 HTML「揉合」在一起
    # 第一個參數要是從瀏覽器送來的 request
    # 第二個參數是要使用的 html 檔案名稱
    # 第三個參數是一個大 Dictionary，把你想傳給 HTML 的變數通通包進去！
    return templates.TemplateResponse(
        request=request, 
        name="w601_hello.html", 
        context={
            "the_name": user_name,  # 餵進去的資料：使用者的名字
            "interest_earned": interest # 餵進去的資料：賺到的利息
        }
    )
