# 경로변수 연습
import logging
from fastapi import FastAPI, Path, Query, status, HTTPException, Request
from datetime import date
from fastapi.responses import JSONResponse
from typing import Dict, Annotated, Optional
from order.presentation.routers.v1.router import router as order_router

logging.basicConfig(level=logging.INFO)
# 로깅 이름은 서버 서비스 명 구분하는 이름으로
logger = logging.getLogger("app") 

app = FastAPI(
    title="1028 경로변수 수업-식료품 재고 관리 시스템",
    description="FastAPI의 Path, Query 매개변수 실습입니다.",
    version="1.0.0"
)

app.include_router(order_router)

# 데이터베이스 대용 임시 메모리 장부
grocery_database: Dict[int, dict] = {
    1: {
        "id": 1,
        "name": "사과",
        "category": "과일",
        "price": 2500,
        "quantity": 80,
        "expiration_date": date(2026, 12, 31)
    },
    2: {
        "id": 2,
        "name": "유기농 우유",
        "category": "유제품",
        "price": 3800,
        "quantity": 1,
        "expiration_date": date(2026, 7, 5)
    }
}

# 유통기한이 지난 식료품은 예외처리
class GroceryExpiredException(Exception):
    def __init__(self, name: str, expiration_date: date):
        self.name = name
        self.expiration_date = expiration_date

# 유통기한 예외 handler 정의
@app.exception_handler(GroceryExpiredException)
async def handle_exception(request: Request, exc: GroceryExpiredException):
        logger.error(f"에러발생: {str(exc)}")

        return JSONResponse(
             status_code = status.HTTP_400_BAD_REQUEST,
             content={
                  "success":False,
                  "message": f"식료품 [{exc.name}]의 유통기한({exc.expiration_date.strftime('%Y년 %m월 %d일')})이 지났습니다."
             }
        )

# 경로변수 넣기
@app.get("/groceries/{item_id}", status_code=status.HTTP_200_OK)
async def get_grocery(
    item_id: Annotated[int, Path(..., description="상품 ID")],
    keyword: Annotated[Optional[str], Query(description="키워드")] = None
):

    
    if item_id not in grocery_database:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "식료품을 찾을 수 없습니다"
        )

    logger.info(f"keyword={keyword}")
    item = grocery_database[item_id]

    if item["expiration_date"] < date.today():
         raise GroceryExpiredException(item['name'], item['expiration_date'])

    return item