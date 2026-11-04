from abc import ABC, abstractmethod
from board.domain.board import Board


class BoardRepository(ABC):
    @abstractmethod
    async def find_by_id(self, board_id: str) -> Board | None:
        """게시판 ID 기준으로 단건 조회 (삭제된 게시판 제외)"""
        pass

    @abstractmethod
    async def find_all(self, include_deleted: bool = False) -> list[Board]:
        """모든 게시판 설정 목록 조회"""
        pass

    @abstractmethod
    async def exists_by_id(self, board_id: str) -> bool:
        """해당 게시판 ID가 이미 존재하는지 여부 확인"""
        pass

    @abstractmethod
    async def save(self, board: Board) -> Board:
        """게시판 설정 등록 또는 수정"""
        pass