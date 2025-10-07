from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKeyConstraint, UniqueConstraint, Identity, PrimaryKeyConstraint, String, \
    text, func, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from datetime import datetime

from app.databases import Base

from uuid import UUID


class File(Base):
    __tablename__ = 'files'
    __table_args__ = (
        ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE', onupdate='CASCADE',
                             name='files_task_id_fkey'),
        PrimaryKeyConstraint('id', name='files_pkey'),
        UniqueConstraint('uuid', name='files_uuid_key')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1,
                                                         maxvalue=9223372036854775807, cycle=False, cache=1),
                                    primary_key=True)
    task_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    original_name: Mapped[str] = mapped_column(String(128), nullable=False)
    uuid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, onupdate=func.now(),
                                                 server_default=text('CURRENT_TIMESTAMP'))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    task: Mapped['Task'] = relationship('Task', back_populates='files')
