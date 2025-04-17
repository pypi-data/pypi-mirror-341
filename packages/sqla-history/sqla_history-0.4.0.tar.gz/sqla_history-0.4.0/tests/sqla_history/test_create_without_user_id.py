import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from sqla_history.context import EventId
from tests.models import Note, OtherHistoryChanges, OtherNote


def test_without_user_id(
    other_note: OtherNote,
    db_session: Session,
) -> None:
    event_id = uuid.uuid4()
    event_token = EventId.set(event_id)

    old_name = other_note.name
    old_description = other_note.description

    new_name = "New name"
    new_description = "New description"

    other_note.name = new_name
    other_note.description = new_description
    db_session.add(other_note)
    db_session.flush()

    stmt = select(cls := OtherHistoryChanges).where(cls.event_id == event_id)
    result = db_session.scalars(stmt).all()

    expected_length = 2

    assert result
    assert len(result) == expected_length

    for item in result:
        if item.field_name == Note.name.key:
            assert item.prev_value == old_name
            assert item.new_value == new_name

        elif item.field_name == Note.description.key:
            assert item.prev_value == old_description
            assert item.new_value == new_description

    EventId.reset(event_token)
