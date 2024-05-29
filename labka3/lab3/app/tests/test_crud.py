from sqlalchemy.orm import Session
import pytest
from unittest.mock import create_autospec
from app.schemes import UserCreate, RecordCreate, UserBase, RecordBase
from app.crud import User_crud, Record_crud
from app.models import User, Record
from typing import Optional


@pytest.fixture
def mock_session() -> Session:
    session = create_autospec(Session)
    return session


def test_create_user(mock_session: Session) -> None:
    user_data = UserCreate(first_name="Test", second_name="User", email="test@example.com", password="password")
    user_crud = User_crud(mock_session)

    mock_user = User(email="test@example.com", first_name="Test", second_name="User", password="hashed_password")
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_user

    created_user = user_crud.create(user_data)

    assert created_user.email == user_data.email
    assert created_user.first_name == user_data.first_name
    assert created_user.second_name == user_data.second_name
    assert created_user.password != user_data.password



def test_get_user(mock_session: Session) -> None:
    user_id = 1
    mock_user = User(id=user_id, email="test@example.com", first_name="Test", second_name="User", password="hashed_password")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    user_crud = User_crud(mock_session)
    retrieved_user = user_crud.get(user_id)

    assert retrieved_user == mock_user


def test_update_user(mock_session: Session) -> None:
    user_id = 1
    user_data = UserBase(first_name="Updated", second_name="User", email="test@example.com")
    mock_user = User(id=user_id, email="test@example.com", first_name="Test",
                     second_name="User", password="hashed_password")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    user_crud = User_crud(mock_session)
    updated_user = user_crud.update(user_id, user_data)

    assert updated_user == mock_user
    assert updated_user.first_name == user_data.first_name
    assert updated_user.second_name == user_data.second_name


def test_delete_user(mock_session: Session) -> None:
    user_id = 1
    mock_user = User(id=user_id, email="test@example.com", first_name="Test",
                     second_name="User", password="hashed_password")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_user

    user_crud = User_crud(mock_session)
    deleted = user_crud.delete(user_id)

    assert deleted is True


def test_create_record(mock_session: Session) -> None:
    record_data = RecordCreate(date="2022-01-01", title="Test Record", content="This is a test record.")
    record_crud = Record_crud(mock_session)

    mock_record = Record(date="2022-01-01", title="Test Record", content="This is a test record.")
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = mock_record

    created_record = record_crud.create(record_data)

    assert created_record.date == record_data.date
    assert created_record.title == record_data.title
    assert created_record.content == record_data.content


def test_get_record(mock_session: Session) -> None:
    record_id = 1
    mock_record = Record(id=record_id, date="2022-01-01", title="Test Record", content="This is a test record.")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_record

    record_crud = Record_crud(mock_session)
    retrieved_record = record_crud.get(record_id)

    assert retrieved_record == mock_record


def test_update_record(mock_session: Session) -> None:
    record_id = 1
    record_data = RecordBase(date="2022-02-01", title="Updated Record", content="This is an updated record.")
    mock_record = Record(id=record_id, date="2022-01-01", title="Test Record", content="This is a test record.")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_record

    record_crud = Record_crud(mock_session)
    updated_record = record_crud.update(record_id, record_data)

    assert updated_record == mock_record
    assert updated_record.date == record_data.date
    assert updated_record.title == record_data.title
    assert updated_record.content == record_data.content


def test_delete_record(mock_session: Session) -> None:
    record_id = 1
    mock_record = Record(id=record_id, date="2022-01-01", title="Test Record", content="This is a test record.")
    mock_session.query.return_value.filter.return_value.first.return_value = mock_record

    record_crud = Record_crud(mock_session)
    deleted = record_crud.delete(record_id)

    assert deleted is True