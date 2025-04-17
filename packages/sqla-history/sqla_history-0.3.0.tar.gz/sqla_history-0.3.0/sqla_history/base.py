from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column
from uuid_utils.compat import uuid7

from .utils import utc_now


class BaseHistoryChanges:
    """
    The base model to inherit from

    Example:
    ```
    from sqlalchemy.orm import DeclarativeBase


    class Base(DeclarativeBase):...


    class HistoryChanges(BaseHistoryChanges, Base):
        user_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id", on_delete="SET NULL"))
        entity_id: Mapped[UUID] = mapped_column(index=True)

    ```
    """

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    event_id: Mapped[UUID] = mapped_column(default=uuid7)
    changed_at: Mapped[datetime] = mapped_column(default=utc_now)
    entity_name: Mapped[str] = mapped_column(String(255), index=True)
    field_name: Mapped[str] = mapped_column(String(255))
    prev_value: Mapped[Any | None] = mapped_column(JSON())
    new_value: Mapped[Any | None] = mapped_column(JSON())
