from contextvars import ContextVar, Token
from uuid import UUID

from .types_ import UserId

current_user_id: ContextVar[UserId | None] = ContextVar("current_user_id", default=None)
"""
A context variable that stores the ID of the user who sent the HTTP request or triggered another action
"""


class CurrentUserId:
    '''Helper class for working with the context variable "current_user_id"'''

    @staticmethod
    def set(value: UserId) -> Token[UserId | None]:
        return current_user_id.set(value)

    @staticmethod
    def get() -> UserId | None:
        return current_user_id.get()

    @staticmethod
    def reset(token: Token[UserId | None]) -> None:
        current_user_id.reset(token)


event_id: ContextVar[UUID | None] = ContextVar("event_id", default=None)
"""
A context variable that stores an event identifier,
by which you can combine changes to fields in database tables (see the `sqla_history.base.BaseHistoryChanges`)
"""


class EventId:
    '''Helper class for working with the context variable "event_id"'''

    @staticmethod
    def set(value: UUID) -> Token[UUID | None]:
        return event_id.set(value)

    @staticmethod
    def get() -> UUID | None:
        return event_id.get()

    @staticmethod
    def reset(token: Token[UUID | None]) -> None:
        event_id.reset(token)
