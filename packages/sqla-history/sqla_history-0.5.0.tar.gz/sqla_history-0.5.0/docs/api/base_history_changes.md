# BaseHistoryChanges

The base model to inherit from

```python
class BaseHistoryChanges:
    """The base model to inherit from"""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    event_id: Mapped[UUID] = mapped_column(default=uuid7)
    changed_at: Mapped[datetime] = mapped_column(default=utc_now)
    entity_name: Mapped[str] = mapped_column(String(255), index=True)
    field_name: Mapped[str] = mapped_column(String(255))
    prev_value: Mapped[Any | None] = mapped_column(JSON())
    new_value: Mapped[Any | None] = mapped_column(JSON())
```
