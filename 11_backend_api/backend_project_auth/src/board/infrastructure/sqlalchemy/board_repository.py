from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from board.domain.board import Board
from board.domain.repository.board_repository import BoardRepository
from board.infrastructure.sqlalchemy.mappers import BoardMapper
from board.infrastructure.sqlalchemy.models import BoardModel

class SqlAlchemyBoardRepository(BoardRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def find_by_id(self, board_id: str) -> Board | None:
        """게시판 ID 기준으로 단건 조회 (삭제된 게시판 제외)"""
        stmt = select(BoardModel).where(
            BoardModel.board_id == board_id,
            BoardModel.deleted_at.is_(None),
        )
        model = await self.session.scalar(stmt)

        return BoardMapper.to_domain(model) if model else None

    async def find_all(self, include_deleted: bool = False) -> list[Board]:
        """모든 게시판 설정 목록 조회"""

        stmt = select(BoardModel)
        if not include_deleted: # 삭제 게시글 미포함
            stmt = stmt.where(BoardModel.deleted_at.is_(None))
        
        models = (await self.session.scalars(stmt)).all()

        return [BoardMapper.to_domain(model) for model in models]

    async def exists_by_id(self, board_id: str) -> bool:
        """해당 게시판 ID가 이미 존재하는지 여부 확인"""
        stmt = select(func.count(BoardModel.board_id)).where(
            BoardModel.board_id == board_id,
            BoardModel.deleted_at.is_(None),
        )

        count = await self.session.scalar(stmt)
        return (count or 0) > 0

    async def save(self, board: Board) -> Board:
        """게시판 설정 등록 또는 수정"""
        _board = await self.session.get(BoardModel, board.board_id)
        if _board: # 게시글이 있다면 수정
            _board.board_name = board.board_name
            _board.page_size = board.page_size
            _board.edit_role = board.authority.edit_role.value
            _board.view_role = board.authority.view_role.value
            _board.list_role = board.authority.list_role.value
            _board.comment_list_role = board.authority.comment_list_role.value
            _board.comment_edit_role = board.authority.comment_edit_role.value
            _board.deleted_at = board.deleted_at
            
            await self.session.flush()
            await self.session.refresh(_board)
            return BoardMapper.to_domain(_board)
        else: # 게시글 등록
            new_model = BoardMapper.to_model(board)
            self.session.add(new_model)

            await self.session.flush()
            await self.session.refresh(new_model)
            return BoardMapper.to_domain(new_model)
        
