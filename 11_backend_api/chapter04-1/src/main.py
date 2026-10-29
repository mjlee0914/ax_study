import logging
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from order.presentation.router import router as order_router
from board.presentation.router import router as board_router
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MIDDLEWARE")

app = FastAPI()

# 모든 HTTP 요청이 API 함수에 도착하기 전과,
# 응답이 브라우저로 돌아가기 전에 거치는 미들웨어 등록
# HTTP request -> middleware -> API func 
# HTTP response -> middleware -> browser
@app.middleware("http")
# call_next: 요청을 다음 단계(API 함수 또는 다음 미들웨어)로 넘기는 함수
async def middleware1(request: Request, call_next):
    logger.info("middleware1()의 요청 처리 전") 
    response = await call_next(request)
    logger.info("middleware1()의 응답 처리 전")

    return response

@app.middleware("http")
async def middleware2(request: Request, call_next):
    logger.info("middleware2()의 요청 처리 전") 
    response = await call_next(request)
    logger.info("middleware2()의 응답 처리 전")

    return response

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"] # 개발환경에서만 접근 가능하도록 세팅
)

# include_router 하나씩만 등록 가능
app.include_router(order_router)
app.include_router(board_router)


