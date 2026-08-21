from sqlalchemy import String,Integer,Boolean,Column
from sqlalchemy.orm import mapped_column,DeclarativeBase,Mapped

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    symbol: Mapped[str] = mapped_column(String(10))
    progress: Mapped[int] = mapped_column(default=0)
    status: Mapped[str] = mapped_column(String(20), default="active")