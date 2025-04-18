import uuid

import pytest

from sqla_history.dto import HistoryCreateDTO
from sqla_history.not_set import NOT_SET, NotSet
from sqla_history.utils import utc_now


@pytest.mark.parametrize(
    "user_id",
    [
        uuid.UUID("cd0c7656-6b41-4094-b4e6-828ab610f668"),
        NOT_SET,
    ],
)
def test_to_dict(user_id: uuid.UUID | NotSet) -> None:
    dto = HistoryCreateDTO(
        event_id=uuid.uuid4(),
        entity_id=888,
        user_id=user_id,
        entity_name="entity_name",
        changed_at=utc_now(),
        field_name="name",
        prev_value=887,
        new_value=888,
    )

    result = dto.to_dict()

    match user_id:
        case uuid.UUID():
            assert result["user_id"]
        case NotSet():
            assert "user_id" not in result
