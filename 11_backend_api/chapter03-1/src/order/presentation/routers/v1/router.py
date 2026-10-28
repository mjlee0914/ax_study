# router.py

from fastapi import APIRouter

# tag 설정 -> 문서 그룹화 가능
# tag는 여러개 묶어도 가능
# tag는 한글도 가능 "주문"
router = APIRouter(prefix="/v1/order", tags=["Orders"])

@router.get("")
async def test1():
	return {"message": "test1"}
	
@router.get("/test")
async def test2():
	return {"message": "test2"}