"""
GET /v1/order -> 주문목록 가져오기
GET /v1/order/{id} -> 주문 상세보기
PATCH /v1/order/{id}/change -> 주문 상태 변경, 상태값이 { status: ... }로 바뀌도록
"""
import logging
from fastapi import APIRouter, Path, Body, Header, HTTPException, Depends
logger=logging.getLogger("TEST")

# 요청 헤더명 X-TOKEN
def verify_secret_token(x_token: str | None = Header(None)):
    if x_token != "secret":
        raise HTTPException(status_code=403, detail="토큰이 잘못되었습니다.")

router = APIRouter(
    prefix="/v1/order", 
    tags=["order", "태그1"], 
    dependencies=[Depends(verify_secret_token)]
    )

def test_func() -> str:
    logger.warning("test_func() 호출")
    return "test_fun"

# GET /v1/order
@router.get("", description="view order list")
async def get_order_list(test:str = Depends(test_func)):
    logger.warning(f"Test: {test}")

# GET /v1/order/{id}
@router.get("/{id}", description="view order detail")
async def get_order_detail(id: int = Path(description="order number")):
    pass

# PATCH /v1/order/{id}/change
@router.patch("/{id}/change", description="change order status", )
async def change_order_status(
    id: int = Path(description="order number"), 
    status: str = Body(description="order status to change")):
    pass