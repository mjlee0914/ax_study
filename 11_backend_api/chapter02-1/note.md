**pydantic**

- 클라이언트가 보낸 데이터를 python 객체로 변환하고 검증하는 도구
- FastAPI가 요청 Body를 검사할 때 주로 사용
- `field_validator`: Field()만으로 표현하기 어려운 특정 필드의 사용자 정의 검증
- `model_validator`: 여러 필드의 관계 또는 모델 전체를 검증할 때 사용
- `Field(..)`: 각 필드의 제약조건과 API 문서용 정보를 정의, 단순한 제약조건에 적합함

```python
# 기본 구조
from pydantic import BaseModel, Field

class BookCreateRequest(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
```

```python
@app.post("/books")
async def create_book(request: BookCreateRequest):
    return {
        "title": request.title,
        "author": request.author
    }
```

```
FastAPI와 Pydantic의 처리 흐름

JSON 요청
   ↓
FastAPI가 BookCreateRequest에 전달
   ↓
Pydantic이 필수 값과 타입 검사 (BaseModel 상속)
   ↓
BookCreateRequest 객체 생성
   ↓
create_book() 실행
```

- class가 BaseModel을 상속, Pydantic은:
  - 요청 데이터 타입 검사
  - 필수 필드 검사
  - 제약조건 검사
  - python 객체 변환
  - 오류 메시지 생성

---

Postman

- 내가 만든 API에 직접 HTTP 요청을 보내고, 응답이 제대로 오는지 테스트하는 도구,
- 임시 클라이언트 역할

---

payload: 클라이언트가 보낸 데이터가 담긴 객체를 받을 수 있도록 함

- HTTP 요청 Body를 BookCreate 규칙으로 검사한 다음, 검증된 객체를 payload 변수에 넣음

```python
# main.py

# 모든 API 요청이 함께 사용하는 임시 책 저장소
books = []

# POST 요청의 JSON Body 전체를 BookCreate Pydantic 모델로 받아서 자동 검증
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate):
    new_book = payload.model_dump()
    books.append(new_book)

    return new_book

@app.get("/books")
async def get_book_all():
    return books
```

```
POST /books → 새로 생성한 책 한 권 반환
GET /books  → 저장된 전체 책 목록 반환
```

- payload: 클라이언트가 보낸 데이터가 담긴 BookCreate 객체
  - payload.title
  - payload.author
  - payload.price

---

```python
def test_fun(a, b, c, *, d, e, f):
    pass
```

- a, b, c: 위치 또는 키워드 매개변수
- d, e, f: 반드시 키워드 매개변수
- `*`: 전달된 값을 저장하지 않고, 단지 매개변수를 구분하는 역할
  EX) test_fun(1, 2, 3, d=4, e=5, f=6)

---

```python
import logging
from typing import Any, Optional, Self

from pydantic import BaseModel, Field, field_validator, model_validator

logger = logging.getLogger(__name__)

class BookCreate(BaseModel):
    # Field: 필드의 필수 여부, 길이, 범위, API 문서 설명 등을 선언한다.
    # ...은 필수 값이라는 뜻이다.
    title: str = Field(..., min_length=2, max_length=100, description="책 제목")
    author: str = Field(..., min_length=2, max_length=50, description="저자")
    # None은 선택 값, gt=0은 값이 있다면 0보다 커야 한다는 뜻이다.
    price: Optional[int] = Field(None, description="가격", gt=0)

    @model_validator(mode="before")
    @classmethod
    def before_validate(cls, data: Any) -> Any:
        # model before: 각 필드가 변환·검증되기 전의 원본 요청 전체를 받는다.
        logger.info("1. model_validator(before) 원본 요청: %s", data)
        return data

    @field_validator("title", "author", mode="before")
    @classmethod
    def trim_text(cls, value: Any) -> Any:
        # field before: Field의 타입·길이 검증 전에 원본 필드 값을 가공한다.
        logger.info("2. field_validator(before) 원본 필드: %r", value)
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("title", "author", mode="after")
    @classmethod
    def check_validated_text(cls, value: str) -> str:
        # field after: 타입 변환과 Field 제약조건을 통과한 필드 값을 받는다.
        logger.info("3. field_validator(after) 검증된 필드: %r", value)
        return value

    @model_validator(mode="after")
    def after_validate(self) -> Self:
        # model after: 모든 필드 검증이 끝난 완성된 BookCreate 객체를 받는다.
        logger.info("4. model_validator(after) 완성된 모델: %s", self)
        return self

# 응답 형식 정의
class BookResponse(BaseModel):
    title: str
    author: str
    price: int
```

```
INFO:book.presentation.schemas:1. model_validator(before) 원본 요청: {'title': '야옹', 'author': '야옹이', 'price': 13222}
INFO:book.presentation.schemas:2. field_validator(before) 원본 필드: '야옹'
INFO:book.presentation.schemas:3. field_validator(after) 검증된 필드: '야옹'
INFO:book.presentation.schemas:2. field_validator(before) 원본 필드: '야옹이'
INFO:book.presentation.schemas:3. field_validator(after) 검증된 필드: '야옹이'
INFO:book.presentation.schemas:4. model_validator(after) 완성된 모델: title='야옹' author='야옹이' price=13222
INFO:book-service:BookCreate: title='야옹' author='야옹이' price=13222
```

- 위 코드를 api app page에서 POST try out 한 결과

---

- logger는 모듈을 따로 만들어서 import 하여 사용하는 것이 좋음. (파일마다 매번 불러올 필요 없도록)
- 다음과 같이 구성 가능

```
chapter02-1/
└── src/
    ├── common/
    │   ├── __init__.py
    │   └── logger.py
    ├── book/
    │   └── presentation/
    │       └── schemas.py
    └── chapter02_1/
        └── main.py
```

```python
# logger.py
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("book-service")
```

```python
# main.py
from common.logger import logger

@app.post("/books")
async def create_book(payload: BookCreate):
    logger.info(f"BookCreate: {payload}")
```

---

`http://127.0.0.1:8000/redoc`

- openAPI UI: API 문서를 읽는 것에 더 중점, test x

`http://127.0.0.1:8000/docs`

- Swagger UI: API 문서 확인과 직접 요청 테스트

`http://127.0.0.1:8000/openapi.json`

- Swagger UI와 ReDoc이 공통으로 사용하는 원본 데이터

```
FastAPI 코드
     ↓
/openapi.json 생성
     ↓
┌─────────────┬─────────────┐
│ Swagger UI  │ ReDoc UI    │
│ /docs       │ /redoc      │
└─────────────┴─────────────┘
```

---

```
TypeScript → <T>
Python     → [T]
```
