import os
import logging
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app") 

app = FastAPI(
    title="1028 jinja2 수업"
)

# template 절대 경로 template engine 설정
# __file__ 은 main.py가 있는 경로 접근
CURRENT_DIR = os.path.dirname(__file__)
# 현재 템플릿 경로와 templates 경로를 join()으로 합침
templates = Jinja2Templates(directory=os.path.join(CURRENT_DIR, "templates"))
templates.env.add_extension("jinja2.ext.do")

@app.get("/practice1", response_class=HTMLResponse)
# 요청에 대한 자세한 정보(헤더/바디 정보)를 포함
async def jinja_practice1(request: Request):
    student_context = {
        "name": "Sparta",
        "age": 20,
        "hobbies": ["독서", "영화"],
        "nickname": None,
        "html_code": "<h2>안녕하세요!</h2>"
    }

    return templates.TemplateResponse(
        request=request, 
        name="practice1.html",
        context=student_context
    )