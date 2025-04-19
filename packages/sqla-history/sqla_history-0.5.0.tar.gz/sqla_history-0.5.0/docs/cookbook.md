# Step by step guide

## Define `HistoryChanges` model

```python
class HistoryChanges(BaseHistoryChanges, Base):
    __tablename__ = "history_changes"

    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    entity_id: Mapped[UUID] = mapped_column(index=True)
```

## Define `"after_update"` handler

```python


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

```

## Set context variables

At the entry point, set the value of the EventId context variable (you can also specify the user ID if you wish.)

```python
from fastapi import APIRouter
from sqla_history.context import CurrentUserId, EventId
from uuid import uuid4

router = APIRouter("/note")

@router.post("/{note_id}")
async def edit_note(
    note_id: UUID,
    schema: NoteEditSchema,
    user_id: UUID = Depends(get_user_id)
    repository: NoteRepository = Depends(get_note_repository),
) -> NoteSchema:
    EventId.set(uuid.uuid4())
    CurrentUserId.set(user_id)

    model = await repository.get(note_id)
    model = await repository.update(model, dto=NoteUpdateDTO.model_validate(schema))

    return NoteSchema.model_validate(model)


```

Check created `HistoryChanges` objects in database
