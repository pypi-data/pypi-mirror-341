# History Model

The `History Model` is used to define the structure of your history changes records. It ensures that every change made to tracked entities is recorded with relevant information such as who made the change and what was changed.

## Fields

- `user_id`: Optional field to track which user made the change.
- `entity_id`: ID of the entity that was changed.

## Example

```python
from sqlalchemy.orm import DeclarativeBase
from sqla_history import BaseHistoryChanges


class Base(DeclarativeBase):...


class HistoryChanges(BaseHistoryChanges, Base):
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("user.id", on_delete="SET NULL"))
    entity_id: Mapped[UUID] = mapped_column(index=True)

```
