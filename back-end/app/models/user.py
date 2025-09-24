from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, DateTime, Identity, Integer, PrimaryKeyConstraint, String, UniqueConstraint, text, Uuid, \
    func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from uuid import UUID

from app.databases import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('uuid', name='users_uuid_key')
    )

    id: Mapped[int] = mapped_column(Integer,
                                    Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647,
                                             cycle=False, cache=1), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    uuid: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, onupdate=func.now(),
                                                 server_default=text('CURRENT_TIMESTAMP'))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    tasks: Mapped[list['Task']] = relationship('Task', back_populates='user')
