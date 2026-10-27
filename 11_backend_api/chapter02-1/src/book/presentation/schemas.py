import logging
from typing import Any, Optional, Self, Generic, TypeVar

from pydantic import BaseModel, Field, field_validator, model_validator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
T = TypeVar("T")


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


# 공통 API response
# 프젝 때에는 /shared에서 공유
# apiresponse는 T라는 type을 받을건데 (아직 type은정해지지않음), 그 type은 data의 type과 일치함.
# main.py에서 APIResponse[...]로 쓰일 때 T가 결정됨.
class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(..., desscription="처리 성공 여부")
    error: Optional[str] = Field(None, description="실패 오류 메시지")

    # data의 타입이 API마다 달라질 수 있다
    data: Optional[T] = Field(None, description="성공시 응답 데이터")
