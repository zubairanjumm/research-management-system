from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    symbol: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    progress: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    resources = relationship(
        "Resource",
        back_populates="project"
    )

    notes = relationship(
        "Note",
        back_populates="project"
    )

    bookmarks = relationship(
        "Bookmark",
        back_populates="project"
    )