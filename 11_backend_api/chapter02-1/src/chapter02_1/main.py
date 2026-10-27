
import logging
from fastapi import FastAPI, HTTPException, Body, status
from pydantic import ValidationError
from typing import Optional, List
from book.presentation.schemas import BookCreate, BookResponse, APIResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("book-service")

app = FastAPI(title="도서 관리 API")


# @app.post("/books", status_code=status.HTTP_201_CREATED)
# async def create_book(
#     title: str = Body(...),
#     author: Optional[str] = Body(None), # optional, 기본값은 None
#     price: int = Body(...)
# ):
#     # 검증실패시 오류 잡기 -> try except
#     try: 
#         book = create_book(title, author, price)
#         logger.info(f"book={book}")
#     except ValidationError as err:
#         logger.error(f"검증 실패: {str(err)}")

# 모든 API 요청이 함께 사용하는 임시 책 저장소
books = []

# POST 요청의 JSON Body 전체를 BookCreate Pydantic 모델로 받아서 자동 검증
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate):
    logger.info(f"BookCreate: {payload}")
    book = payload.model_dump(exclude_unset=True) # 사용자가 입력한 값만 추출
    books.append({
        "title": payload.title,
        "author": payload.author,
        "price": payload.price
    })
    logger.info(f"Book: {payload}, type: {type(book)}, 제목: {payload.title}")

# APIResponse[List[BookResponse]]는 BookResponse의 목록을 담는다
# APIResponse의 type은 BookResponse '목록' 이다.
@app.get("/books", response_model=APIResponse[List[BookResponse]]) # APIResponse[T] => T = list[BookResponse]
async def get_book_all():
    return APIResponse(sucess=True, data=books)
