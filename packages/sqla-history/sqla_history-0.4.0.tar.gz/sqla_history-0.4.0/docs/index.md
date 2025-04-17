# SQLAlchemy History

SQLAlchemy History is an extension for SQLAlchemy that provides change tracking and history logging for SQLAlchemy models. It allows developers to easily track changes to their database objects over time, providing a comprehensive history of modifications.

## Features

- Track changes made to SQLAlchemy models.
- Log historical data for audit purposes.
- Easily integrate with existing SQLAlchemy applications.

## How it works

When you change model fields and add the model to a session, via `session.add(model)` or `session.add_all([model])`, the event listener `"after_update"` you defined is triggered.

This listener monitors for changes to field values. If changes have been made, an object containing the field changes (`HistoryChanges`) will be added to the corresponding table.

## Step by step guide

1. Define `HistoryChanges` model
2. Define `"after_update"` handler
3. At the entry point, set the value of the EventId context variable (you can also specify the user ID if you wish.)
4. Check created `HistoryChanges` objects in database

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
