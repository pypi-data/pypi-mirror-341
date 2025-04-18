# Event Listener

Event listeners are crucial for tracking changes to SQLAlchemy models. They allow the application to respond to changes in the database by recording them in history.

## Creating an Event Listener

To create an event listener, you need to define it in the same module as the model and listen for the `"after_update"` event.

### Example

```python
@event.listens_for(Note, "after_update")
def create_note_history(mapper: Mapper, connection: Connection, target: Note) -> None:
    # Implementation details
```
