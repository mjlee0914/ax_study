import logging
from typing import Optional # 매개변수 필수가 아님을 나타낼 때 사용
from fastapi import FastAPI, Body, Query, HTTPException, status

# book.py 안의 Book 클래스를 main.py로 가져옴
# main.py에서 Book.create() 사용 가능 
from book.domain.book import Book
# main.py 역할: FastAPI 영역, 외부 HTTP 요청을 받는 입구

# 책 추가 및 조회만 구현

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("Book App")

#브라우저
#   ↓ GET /books
#FastAPI
#   ↓ get_books() 실행
#["Book A0", "Book B"]
#   ↓ JSON 변환
#브라우저에 응답

# FastAPI()를 사용하여 python 프로그램이 웹 요청을 받는 API app으로 만듦.
# browser가 HTTP요청을 통해 함수를 실행할 수 있음

# 설명 꼼꼼하게 달기 - title(1st param), description(2nd param)
app = FastAPI(
    title="도서 대출 서비스",
    description="도서 대출 서비스 연습",
    version="0.0.1"
)

in_memory_db: dict = {}
id_generator: int = 1

# post 성공시 201 상태 메시지
# "when a POST request hits /books..."
@app.post("/books", status_code=status.HTTP_201_CREATED)
# "...run this function"
async def create_book(
    title: str = Body(..., description="등록할 책 이름"), # (...) -> 필수 항목. 값이 들어오지 않으면 420 오류
    author: str = Body(..., description="등록할 책 저자명")
):
    global id_generator
    logger.info(f"신규 도서 등록: 제목={title} 저자={author}")

    try:
        new_book = Book.create(id_generator, title, author, 'AVAILABLE')
        logger.info(f"신규 도서 등록 성공: 제목={title} 저자={author}")
        id_generator += 1
        return new_book.to_dict()

    except ValueError as err:
        logger.error(f"신규 도서 등록 실패: {str(err)}") # 에러메시지 출력, 꼼꼼히!
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

# http://127.0.0.1:8000/books?search_keyword=...
@app.get("/books")
                                    # search_keyword is optional string, if not Null
                                    # 설정시 uv terminal: 
                                    # INFO:     127.0.0.1:52855 - "GET /books HTTP/1.1" 200 OK
                                    # INFO:Book App:search_keyword: None
                                    # Query(alias)설정 시 주소창에 search_keyword대신 keyword 입력 가능
                                    # Query(min_length=2)일 시 http://127.0.0.1:8000/books?keyword=1 이면 오류
async def get_all_books(search_keyword:Optional[str] = Query(None, alias="keyword", description="검색 키워드", min_length=2)):
    # search_keyword = search params
    logger.info(f"search_keyword: {search_keyword}")