from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, DateTime, CheckConstraint, ForeignKeyConstraint, Identity, Integer, \
    PrimaryKeyConstraint, SmallInteger, String, Text, text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime, date

from app.databases import Base


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        CheckConstraint('status = ANY (ARRAY[0, 1, 2])', name='tasks_status_check'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE',
                             name='tasks_user_id_fkey'),
        PrimaryKeyConstraint('id', name='tasks_pkey')
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True, start=1, increment=1, minvalue=1,
                                                         maxvalue=9223372036854775807, cycle=False, cache=1),
                                    primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    deadline: Mapped[Optional[date]] = mapped_column(Date)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                 server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, onupdate=func.now(),
                                                 server_default=text('CURRENT_TIMESTAMP'))
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    user: Mapped['User'] = relationship('User', back_populates='tasks')
    files: Mapped[list['File']] = relationship('File', back_populates='task')
