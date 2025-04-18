from types import SimpleNamespace
from uuid import UUID

from sqla_history import (
    BaseHistoryChanges,
    InsertStmtBuilder,
    WithUserChangeEventHandler,
)
from sqlalchemy import Connection, ForeignKey, MetaData, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, Mapper, mapped_column
from uuid_utils.compat import uuid7

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


class Base(DeclarativeBase):
    metadata = meta


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)


class HistoryChanges(BaseHistoryChanges, Base):
    __tablename__ = "history_changes"

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    entity_id: Mapped[UUID] = mapped_column(index=True)


class Note(Base):
    __tablename__ = "note"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))


class EntityName(SimpleNamespace):
    note = "note"


@event.listens_for(Note, "after_update")
def create_note_history(
    mapper: Mapper,
    connection: Connection,
    target: Note,
) -> None:
    stmt_builder = InsertStmtBuilder(history_model=HistoryChanges)
    handler = WithUserChangeEventHandler(
        entity_name=EntityName.note,
        stmt_builder=stmt_builder,
    )
    handler(mapper=mapper, connection=connection, target=target)
