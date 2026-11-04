import uuid
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

#from auth.application.service import AuthService
from shared.core.database import get_db
from shared.core.exceptions import ForbiddenException, UnauthorizedException
from user.application.service import UserService
from user.domain.repository import UserRepository
from user.domain.service import PasswordHasher
from user.domain.user import User
from user.infrastructure.repositories import SqlAlchemyUserRepository
from user.infrastructure.security import BcryptPasswordHasher
from user.presentation.dependencies import (
    get_current_user,
    provide_user_repository,
    provide_user_service,
    require_admin,
)

bearer_security = HTTPBearer(auto_error=True)
password_hasher: PasswordHasher = BcryptPasswordHasher()


def create_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def create_user_service(
    repository: UserRepository = Depends(create_user_repository),
) -> UserService:
    return UserService(repository=repository, hasher=password_hasher)


async def resolve_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_security)],
    user_repo: Annotated[UserRepository, Depends(create_user_repository)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    from wiring.auth import create_auth_service
    auth_service: AuthService = create_auth_service(session=session, user_repository=user_repo)

    payload = await auth_service.authenticate_token(credentials.credentials)
    user = await user_repo.find_by_id(uuid.UUID(str(payload.user_id)))
    if not user:
        raise UnauthorizedException("존재하지 않는 사용자입니다.")
    if getattr(user, "resign", False):
        raise ForbiddenException(
            message="탈퇴한 회원은 서비스를 이용할 수 없습니다.",
            error_code="USER_ALREADY_WITHDRAWN",
        )
    return user


async def resolve_require_admin(
    current_user: Annotated[User, Depends(resolve_current_user)],
) -> User:
    if current_user.role != "ADMIN":
        raise ForbiddenException(
            message="관리자 권한이 필요합니다.",
            error_code="ADMIN_PERMISSION_DENIED",
        )
    return current_user


def wire_user_dependencies(app: FastAPI) -> None:
    app.dependency_overrides.update(
        {
            provide_user_repository: create_user_repository,
            provide_user_service: create_user_service,
            get_current_user: resolve_current_user,
            require_admin: resolve_require_admin,
        }
    )