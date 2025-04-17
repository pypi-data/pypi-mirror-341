from types import SimpleNamespace
from uuid import UUID

from sqlalchemy import Connection, ForeignKey, MetaData, String, event
from sqlalchemy.orm import DeclarativeBase, Mapped, Mapper, mapped_column
from uuid_utils.compat import uuid7

from sqla_history import (
    BaseHistoryChanges,
    InsertStmtBuilder,
    WithUserChangeEventHandler,
)
from sqla_history.event_handlers import ChangeEventHandler

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


class EntityName(SimpleNamespace):
    note = "note"
    note2 = "note2"
    note3 = "note3"
    other_note = "other_note"


class Note(Base):
    __tablename__ = "note"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))


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


class Note2(Base):
    __tablename__ = "note2"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))


@event.listens_for(Note2, "after_update")
def create_note_history_with_tracking_fields(
    mapper: Mapper,
    connection: Connection,
    target: Note2,
) -> None:
    stmt_builder = InsertStmtBuilder(history_model=HistoryChanges)
    handler = WithUserChangeEventHandler(
        entity_name=EntityName.note2,
        stmt_builder=stmt_builder,
        tracking_fields=(Note2.description,),
    )
    handler(mapper=mapper, connection=connection, target=target)


class Note3(Base):
    __tablename__ = "note3"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))


@event.listens_for(Note3, "after_update")
def create_note_history_with_ignored_fields(
    mapper: Mapper,
    connection: Connection,
    target: Note3,
) -> None:
    stmt_builder = InsertStmtBuilder(history_model=HistoryChanges)
    handler = WithUserChangeEventHandler(
        entity_name=EntityName.note3,
        stmt_builder=stmt_builder,
        ignored_fields=(Note3.description,),
    )
    handler(mapper=mapper, connection=connection, target=target)


class OtherHistoryChanges(BaseHistoryChanges, Base):
    __tablename__ = "other_history_changes"

    entity_id: Mapped[UUID] = mapped_column(index=True)


class OtherNote(Base):
    __tablename__ = "other_note"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    is_active: Mapped[bool] = mapped_column(default=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(512))


@event.listens_for(OtherNote, "after_update")
def create_other_note_history_without_user(
    mapper: Mapper,
    connection: Connection,
    target: OtherNote,
) -> None:
    stmt_builder = InsertStmtBuilder(history_model=OtherHistoryChanges)
    handler = ChangeEventHandler(
        entity_name=EntityName.other_note,
        stmt_builder=stmt_builder,
    )
    handler(mapper=mapper, connection=connection, target=target)
