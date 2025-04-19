import pprint
from collections.abc import Iterator
from contextlib import contextmanager

from sqla_history.context import CurrentUserId, EventId
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from uuid_utils.compat import uuid7

from . import models

engine = create_engine("sqlite:///:memory:")
session_factory = sessionmaker(bind=engine)

OLD_NAME = "Name"
OLD_DESCRIPTION = "Description"

NEW_NAME = "Changed Name"
NEW_DESCRIPTION = "NANIIIIIIIII"


@contextmanager
def create_db() -> Iterator[None]:
    models.Base.metadata.create_all(engine)
    yield
    models.Base.metadata.clear()


def main() -> None:
    with create_db(), session_factory.begin() as session:
        # Creation of User and Note
        user = models.User()
        note = models.Note(name=OLD_NAME, description=OLD_DESCRIPTION)
        session.add_all((user, note))
        session.flush()

        # The context variable must be set to `current_user_id``
        CurrentUserId.set(user.id)

        # The context variable must be set to `event_id`
        event_id = uuid7()
        EventId.set(event_id)

        # Applying changes
        note = _mutate_note(note)
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


def _mutate_note(note: models.Note) -> models.Note:
    note.name = NEW_NAME
    note.description = NEW_DESCRIPTION
    return note


if __name__ == "__main__":
    main()
