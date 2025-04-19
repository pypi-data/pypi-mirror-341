from collections.abc import Sequence
from datetime import datetime
from logging import getLogger
from typing import Any
from uuid import UUID

from sqlalchemy import Column, Connection, inspect
from sqlalchemy.orm import DeclarativeBase, InstanceState, InstrumentedAttribute, Mapper

from sqla_history.stmt_builder import InsertStmtBuilder

from .context import CurrentUserId, EventId
from .dto import HistoryCreateDTO, Value
from .not_set import NOT_SET, NotSet
from .types_ import UserId
from .utils import utc_now

logger = getLogger(__name__)


class ChangeEventHandler:
    """
    Handler for tracking changes in a database entity and building
    corresponding insert statements for history logging.

    Args:
        entity_name (str): The name of the entity being tracked.
        stmt_builder (InsertStmtBuilder): The statement builder used to create
                                           insert statements for history records.
        id_field_name (str): The name of the primary key field in the entity.
                             Defaults to "id".
        tracking_fields (Sequence[InstrumentedAttribute[Any]] | None): The fields to track
                                                                      changes for. If None,
                                                                      all fields will be tracked.
        ignored_fields (Sequence[InstrumentedAttribute[Any]] | None): The fields to ignore
                                                                     when tracking changes.
                                                                     If None, no fields will be ignored.
    """

    def __init__(
        self,
        entity_name: str,
        stmt_builder: InsertStmtBuilder,
        id_field_name: str = "id",
        tracking_fields: Sequence[InstrumentedAttribute[Any]] | None = None,
        ignored_fields: Sequence[InstrumentedAttribute[Any]] | None = None,
    ) -> None:
        self._entity_name = entity_name
        self._stmt_builder = stmt_builder
        self._id_field_name = id_field_name
        self._tracking_fields = tuple(item.key for item in (tracking_fields or ()))
        self._ignored_fields = tuple(item.key for item in (ignored_fields or ()))

    def __call__(
        self,
        mapper: Mapper,
        connection: Connection,
        target: DeclarativeBase,
    ) -> None:
        """
        Handle the change event for the target entity.

        Args:
            mapper (Mapper): The mapper associated with the target entity.
            connection (Connection): The database connection to execute the statement.
            target (DeclarativeBase): The target entity instance that has changed.

        Returns:
            None: This method does not return a value. It executes an insert statement
                  if changes are detected.
        """
        if (event_id := EventId.get()) is None:
            logger.info("event_id is None. Changes wasn't tracked")
            return

        state = inspect(target)
        pk = getattr(target, self._id_field_name)
        changed_at = utc_now()

        dtos = self._construct_dtos(
            mapper=mapper,
            target=target,
            event_id=event_id,
            state=state,
            pk=pk,
            changed_at=changed_at,
        )

        if not dtos:
            return

        stmt = self._stmt_builder.build(dtos)
        connection.execute(stmt)

    def _construct_dtos(  # noqa: PLR0913
        self,
        mapper: Mapper,
        target: DeclarativeBase,
        event_id: UUID,
        state: InstanceState[DeclarativeBase],
        pk: UUID,
        changed_at: datetime,
    ) -> Sequence[HistoryCreateDTO]:
        """
        Construct DTOs for the changes detected in the target entity.

        Args:
            mapper (Mapper): The mapper associated with the target entity.
            target (DeclarativeBase): The target entity instance.
            event_id (UUID): The ID of the event tracking the changes.
            state (InstanceState[DeclarativeBase]): The state of the target entity.
            pk (UUID): The primary key of the target entity.
            changed_at (datetime): The timestamp of when the change occurred.

        Returns:
            Sequence[HistoryCreateDTO]: A list of DTOs representing the changes.
        """
        return [
            dto
            for attr in mapper.columns
            if not self._is_field_ignored(attr)
            and self._is_field_tracked(attr)
            and (
                dto := self._construct_dto(
                    attr=attr,
                    target=target,
                    event_id=event_id,
                    state=state,
                    pk=pk,
                    changed_at=changed_at,
                )
            )
            is not None
        ]

    def _is_field_ignored(self, attr: Column[Any]) -> bool:
        """
        Check if a given attribute is in the list of ignored fields.

        Args:
            attr (Column[Any]): The attribute to check.

        Returns:
            bool: True if the attribute is ignored, False otherwise.
        """
        return attr.key in self._ignored_fields

    def _is_field_tracked(self, attr: Column[Any]) -> bool:
        """
        Check if a given attribute is in the list of tracked fields.

        Args:
            attr (Column[Any]): The attribute to check.

        Returns:
            bool: True if the attribute is tracked, False otherwise.
        """
        if not self._tracking_fields:
            return True

        return attr.key in self._tracking_fields

    def _construct_dto(  # noqa: PLR0913
        self,
        attr: Column[Any],
        target: DeclarativeBase,
        event_id: UUID,
        state: InstanceState[DeclarativeBase],
        pk: UUID,
        changed_at: datetime,
    ) -> HistoryCreateDTO | None:
        """
        Construct a DTO for a single changed attribute.

        Args:
            attr (Column[Any]): The attribute of model.
            target (DeclarativeBase): The target entity instance.
            event_id (UUID): The ID of the event tracking the changes.
            state (InstanceState[DeclarativeBase]): The state of the target entity.
            pk (UUID): The primary key of the target entity.
            changed_at (datetime): The timestamp of when the change occurred.

        Returns:
            HistoryCreateDTO | None: A DTO representing the change, or None if no change
                                      is detected.
        """
        field_name = attr.key
        new_value = getattr(target, field_name)
        attribute_state = state.attrs[field_name]
        if not attribute_state.history.deleted:
            return None

        prev_value = attribute_state.history.deleted[0]
        if prev_value == new_value:  # pragma: no cover
            # no cover as the case could not be reproduced
            return None

        return HistoryCreateDTO(
            event_id=event_id,
            entity_id=pk,
            entity_name=self._entity_name,
            changed_at=changed_at,
            field_name=field_name,
            prev_value=Value(prev_value).model_dump(mode="json"),
            new_value=Value(new_value).model_dump(mode="json"),
            user_id=self._get_user_id(),
        )

    def _get_user_id(self) -> UserId | None | NotSet:
        """
        Retrieve the user ID associated with the change event.

        Returns:
            NotSet in current implementation.
        """
        return NOT_SET


class WithUserChangeEventHandler(ChangeEventHandler):
    def _get_user_id(self) -> UserId | None | NotSet:
        """
        Retrieve the user ID associated with the change event.

        Returns:
            UserId | None in current implementation.
        """
        return CurrentUserId.get()
