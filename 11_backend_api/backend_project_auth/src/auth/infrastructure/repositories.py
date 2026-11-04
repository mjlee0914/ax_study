from datetime import datetime
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.repository import TokenBlacklistRepository
from auth.infrastructure.models import TokenBlacklistModel

class SqlAlchemyTokenBlacklistRepository(TokenBlacklistRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, jti: str, expired_at: datetime) -> None:
        """블랙리스트에 토큰 식별자 등록"""
        blacklist_item = TokenBlacklistModel(jti=jti, expired_at=expired_at)
        self.session.add(blacklist_item)
        await self.session.flush() 
        # flush()
        # 현재 세션에 쌓인 변경 사항을 모아서 DB에 SQL로 전송한다
        # 트랜잭션 최종 확정은 아님 -> commit()과 다름
        # 요청 전체가 성공하면 commit
        # 요청 중 오류 생기면 rollback

    async def is_blacklisted(self, jti: str) -> bool:
        """토큰이 블랙리스트에 등록되어 있는지 확인"""
        stmt = select(TokenBlacklistModel.jti).where(TokenBlacklistModel.jti == jti)
        result = await self.session.scalar(stmt) 
        return result is not None

    async def cleanup_expired(self, current_time: datetime) -> int:
        """유효기간이 지난 블랙리스트 항목 정리"""
        stmt= delete(TokenBlacklistModel).where(TokenBlacklistModel.expired_at <= current_time)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount
        
     