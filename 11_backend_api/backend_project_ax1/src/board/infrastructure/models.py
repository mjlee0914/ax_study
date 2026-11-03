from datetime import datetime,timezone
from sqlalchemy import String, Text, BigInteger, Integer, DateTime, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.core.models import Base


class Board(Base):
    """게시판 설정"""
    __tablename__ = "boards"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(65), nullable=False)
    write_role: Mapped[str] = mapped_column(String(30), default="ALL", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    modified_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    """
    lazy: raise 기본값, 가져오지 않음
           selectin : 1: N -> 1차 쿼리 ->  in 조건으로 2차 쿼리 수행 
           joined : N:1 -> 처음부터 LEF JOIN 
    """
    posts: Mapped[list["Post"]] = relationship(
        back_populates="board_config",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

#다대다 관계를 위한 중간 테이블
post_tag_association = Table(
    "posts_tags",
    Base.metadata,
    Column(
        "post_id",
        BigInteger,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        BigInteger,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )
)

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )

    category: Mapped[str] = mapped_column(
        String(60),
        nullable=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    modified_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # 외래키 
    board_id: Mapped[str] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 게시판 설정(N:1)
    board_config: Mapped["Board"] = relationship(
        back_populates="posts",
        lazy="joined"
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tag_association,
        back_populates="posts",
        lazy="selectin"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content 
        }

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=True, index=True)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tag_association,
        back_populates="tags",
        lazy="selectin"
    )
    