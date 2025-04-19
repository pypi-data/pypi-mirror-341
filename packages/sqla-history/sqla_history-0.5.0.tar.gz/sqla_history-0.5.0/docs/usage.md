# Usage

## Implementation HistoryChanges Model

Define the model and ensure to include the `entity_id` field. Optionally, you can define a foreign key field with a User ID to track who made changes to the model.

### Example

```python
from sqla_history import BaseHistoryChanges

class Base(DeclarativeBase):
    metadata = meta

class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)

class HistoryChanges(BaseHistoryChanges, Base):
    __tablename__ = "history_changes"

    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id", ondelete="SET NULL"))
    entity_id: Mapped[UUID] = mapped_column(index=True)
```

### Creating event listener

In this step you need to create an event listener with `"after_update"` type.

Example:

```python
# models.py

from sqlalchemy import Connection, String, event
from sqlalchemy.orm import Mapped, Mapper
from sqla_history import InsertStmtBuilder, WithUserChangeEventHandler

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
        entity_name="note",
        stmt_builder=stmt_builder,
    )
    handler(mapper=mapper, connection=connection, target=target)
```

Now change the field format of your model, call `session.flush()`, and check that the field records appear in the database.

```python
# main.py


def _mutate_note(note: models.Note) -> models.Note:
note.name = NEW_NAME
note.description = NEW_DESCRIPTION
return note

def main() -> None:
session: Session = ... # resolve session
user: models.User = ... # resolve model from DB
note: models.Note = ... # resolve model from DB

    # The context variable must be set to `current_user_id``
    CurrentUserId.set(user.id)

    # The context variable must be set to `event_id`
    event_id = uuid7()
    EventId.set(event_id)

    # Applying changes
    note = _mutate_note(note) # mutation note (name, description)
    session.add(note)
    session.flush()

    # Searching HistoryChanges
    stmt = select(cls := models.HistoryChanges).where(cls.event_id == event_id)
    result = session.scalars(stmt).all()

    assert result

    for item in result:
        if item.field_name == models.Note.name.key:
            assert item.prev_value == OLD_NAME
            assert item.new_value == NEW_NAME

        elif item.field_name == models.Note.description.key:
            assert item.prev_value == OLD_DESCRIPTION
            assert item.new_value == NEW_DESCRIPTION

        pprint.pprint(
            {
                "id": str(item.id),
                "user_id": str(item.user_id),
                "entity_id": str(item.entity_id),
                "event_id": str(item.event_id),
                "changed_at": item.changed_at.isoformat(),
                "entity_name": item.entity_name,
                "field_name": item.field_name,
                "prev_value": item.prev_value,
                "new_value": item.new_value,
            },
            sort_dicts=False,
            indent=2,
        )

```

```

```
