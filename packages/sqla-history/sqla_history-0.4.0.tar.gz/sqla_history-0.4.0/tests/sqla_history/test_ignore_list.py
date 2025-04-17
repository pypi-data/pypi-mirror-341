import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from sqla_history.context import CurrentUserId, EventId
from tests.models import (
    HistoryChanges,
    Note3,
    User,
)


def test_ignore_list(user: User, note_3: Note3, db_session: Session) -> None:
    event_id = uuid.uuid4()
    event_token = EventId.set(event_id)
    user_token = CurrentUserId.set(user.id)

    old_name = note_3.name

    new_name = "New name"
    new_description = "New description"

    note_3.name = new_name
    note_3.description = new_description
    db_session.add(note_3)
    db_session.flush()

    stmt = select(cls := HistoryChanges).where(cls.event_id == event_id)
    result = db_session.scalars(stmt).all()

    expected_length = 1

    assert result
    assert len(result) == expected_length

    item = result[0]
    assert item.field_name == Note3.name.key
    assert item.prev_value == old_name
    assert item.new_value == new_name

    CurrentUserId.reset(user_token)
    EventId.reset(event_token)
