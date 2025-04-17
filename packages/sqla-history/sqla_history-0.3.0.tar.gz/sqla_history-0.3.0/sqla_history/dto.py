from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import RootModel

from .not_set import NOT_SET, NotSet
from .types_ import EntityId, UserId


class Value(RootModel[Any]):
    pass


@dataclass(frozen=True, slots=True, kw_only=True)
class HistoryCreateDTO:
    """
    Data Transfer Object (DTO) for logging changes to an entity in the history.

    This class is used to represent a change event, capturing details about the
    change, including the previous and new values of the changed field.
    """

    event_id: UUID
    entity_id: EntityId
    user_id: UserId | None | NotSet = NOT_SET
    entity_name: str
    changed_at: datetime
    field_name: str
    prev_value: Any
    new_value: Any

    def to_dict(self) -> Mapping[str, Any]:
        data = asdict(self)
        if isinstance(self.user_id, NotSet):
            del data["user_id"]

        return data
