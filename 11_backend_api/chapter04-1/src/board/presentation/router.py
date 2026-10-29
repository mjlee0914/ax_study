from fastapi import APIRouter, Path

# APIRouter 불러올 때 prefix 필수
# 기능 업데이트 등 바뀔 때 기존 서비스 유지해야 함. 버전관리해야함.
router = APIRouter(prefix="/v1/board", tags=["board", "태그1"])

# GET /v1/board
@router.get("", description="view board config")
async def get_board_config():
    pass

# PUT /v1/board/edit
@router.post("/{id}/edit", description="edit post")
async def edit_post(id: int = Path(description="post number")):
    pass
