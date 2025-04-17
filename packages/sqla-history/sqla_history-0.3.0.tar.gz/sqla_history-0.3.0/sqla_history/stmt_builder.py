from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Final, final

from sqlalchemy import Insert, insert
from sqlalchemy.orm import DeclarativeBase

from .dto import HistoryCreateDTO


class BaseInsertStmtBuilder(ABC):  # pragma: no cover
    """
    Abstract class for building SQL INSERT statements for history models.

    This class provides basic functionality for validating the presence of an
    entity ID field and serves as a foundation for specific implementations of
    insert statement builders.

    Attributes:
        _entity_id_field (Final[str]): The name of the entity ID field that must be
                                   defined in the history model.

    Args:
        history_model (type[DeclarativeBase]): The class of the history model that
                                                must contain the entity ID field.

    Raises:
        ValueError: If the entity ID field is not defined in the model.

    Example usage:
    ```
    class HistoryChanges(BaseHistoryChanges, Base):
        __tablename__ = "history_changes"

        user_id: Mapped[UUID | None] = mapped_column(
            ForeignKey("user.id", ondelete="SET NULL")
        )
        entity_id: Mapped[UUID] = mapped_column(index=True)

    ...


    @event.listens_for(Note, "after_update")
    def create_note_history(
        mapper: Mapper,
        connection: Connection,
        target: Note,
    ) -> None:
        stmt_builder = InsertStmtBuilder(history_model=HistoryChanges)
        ...
    ```
    """

    _entity_id_field: Final = "entity_id"

    def __init__(self, history_model: type[DeclarativeBase]) -> None:
        """
        Initializes BaseInsertStmtBuilder with the specified history model.

        Args:
            history_model (type[DeclarativeBase]): The class of the history model.

        Raises:
            ValueError: If the model does not contain the entity ID field.
        """

        self._validate_model(history_model)

        self._history_model = history_model

    def _validate_model(self, cls: type[DeclarativeBase]):
        """
        Validates that the model contains the specified entity ID field.

        Args:
            cls (type[DeclarativeBase]): The class of the history model to validate.

        Raises:
            ValueError: If the entity ID field is not defined in the model.
        """

        if not hasattr(cls, self._entity_id_field):
            msg = f'Define "{self._entity_id_field}" field in {cls.__qualname__}'
            raise ValueError(msg)

    @abstractmethod
    def build(
        self,
        dtos: Sequence[HistoryCreateDTO],
    ) -> Insert:
        """
        Build an INSERT statement based on the provided DTOs.

        Args:
            dtos (Sequence[HistoryCreateDTO]): A list of DTO objects containing the
                                                data to insert.

        Returns:
            Insert: An INSERT statement for execution in the database.
        """


@final
class InsertStmtBuilder(BaseInsertStmtBuilder):
    def build(
        self,
        dtos: Sequence[HistoryCreateDTO],
    ) -> Insert:
        return insert(self._history_model).values([dto.to_dict() for dto in dtos])
