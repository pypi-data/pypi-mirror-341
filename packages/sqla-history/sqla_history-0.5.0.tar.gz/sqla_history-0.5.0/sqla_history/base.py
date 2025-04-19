from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from .utils import utc_now

try:
    from uuid_utils.compat import uuid7 as generate_uuid
except ImportError:  # pragma: no cover
    from uuid import uuid4 as generate_uuid  # type: ignore[assignment]


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

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=generate_uuid,
        comment="Identifier",
    )
    event_id: Mapped[UUID] = mapped_column(
        default=generate_uuid,
        comment="The event ID that will be used to merge records with field changes",
    )
    changed_at: Mapped[datetime] = mapped_column(
        default=utc_now, comment="Date and time of field change"
    )
    entity_name: Mapped[str] = mapped_column(
        String(255),
        index=True,
        comment="Name of the entity whose field is being changed",
    )
    field_name: Mapped[str] = mapped_column(
        String(255),
        comment="The name of the field that is being changed",
    )
    prev_value: Mapped[Any | None] = mapped_column(
        JSON(),
        comment="Previous field value",
    )
    new_value: Mapped[Any | None] = mapped_column(JSON(), comment="New field value")
