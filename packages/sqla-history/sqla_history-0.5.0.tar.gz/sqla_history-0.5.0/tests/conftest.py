from collections.abc import Iterable, Iterator
from typing import TypeVar

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Note, Note2, Note3, OtherNote, User


@pytest.fixture(scope="session")
def db_engine() -> Iterable[Engine]:
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
def session_factory(db_engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=db_engine)


@pytest.fixture
def db_session(
    create_db: None,  # noqa: ARG001
    db_engine: Engine,
    session_factory: sessionmaker[Session],
) -> Iterable[Session]:
    with db_engine.connect() as connection:
        transaction = connection.begin()
        session_factory.configure(bind=connection)

        with session_factory() as session:
            yield session

        if transaction.is_active:
            transaction.rollback()


@pytest.fixture(scope="session")
def create_db(db_engine: Engine) -> Iterator[None]:
    Base.metadata.create_all(db_engine)
    yield
    Base.metadata.clear()


@pytest.fixture
def user(db_session: Session) -> User:
    model = User()
    db_session.add(model)
    db_session.flush()
    return model


_TModel = TypeVar("_TModel", bound=Note | Note2 | Note3 | OtherNote)


def _create_note(
    db_session: Session,
    cls: type[_TModel],
) -> _TModel:
    model = cls(name="Note name", description="Note description")
    db_session.add(model)
    db_session.flush()
    return model  # type: ignore[return-value]


@pytest.fixture
def note(db_session: Session) -> Note:
    return _create_note(db_session, Note)


@pytest.fixture
def note_2(db_session: Session) -> Note2:
    return _create_note(db_session, Note2)


@pytest.fixture
def note_3(db_session: Session) -> Note3:
    return _create_note(db_session, Note3)


@pytest.fixture
def other_note(db_session: Session) -> OtherNote:
    return _create_note(db_session, OtherNote)
