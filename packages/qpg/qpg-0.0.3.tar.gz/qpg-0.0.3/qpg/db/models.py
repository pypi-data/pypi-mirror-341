from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import JSON, func
from sqlalchemy.dialects.postgresql import TIMESTAMP


class Base(DeclarativeBase):
    pass
    

class Queue(Base):
    __tablename__ = "queue"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(nullable=False)
    queue_name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    state: Mapped[str] = mapped_column(default='add')
    dt: Mapped[str] = mapped_column(TIMESTAMP, default=func.now())
