import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.repository.users import UserRepository


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture
def user_repository(mock_session):
    return UserRepository(mock_session)


@pytest.fixture
def contact():
    return Contact(id=1, email="sky@walker.com")


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, mock_session):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = User(id=1, username="Luke")
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    user = await user_repository.get_user_by_id(user_id=1)
    # Assertions
    assert user is not None
    assert user.id == 1
    assert user.username == "Luke"


@pytest.mark.asyncio
async def test_get_user_by_username(user_repository, mock_session):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = User(id=1, username="Luke")
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    user = await user_repository.get_user_by_username(username="tutu")
    # Assertions
    assert user is not None
    assert user.id == 1
    assert user.username == "Luke"


# get_user_by_username
# get_user_by_email
# create_user
# confirmed_email
# update_avatar_url


# @pytest.mark.asyncio
# async def test_create_contact(contact_repository, mock_session, user):
#     contact_data = ContactBase(
#         email="sky@walker.com",
#         first_name="Luke",
#         last_name="Skywalker",
#         phone="40358974",
#         birth_date=datetime(day=25, month=2, year=1999),
#         additional=""
#     )
#
#     # Call method
#     created_contact = await contact_repository.create_contact(contact_data, user=user)
#
#     # Assertions
#     assert created_contact is not None
#     assert isinstance(created_contact, Contact)
#     assert created_contact.first_name == "Luke"
#     assert created_contact.email == "sky@walker.com"
#
#
# @pytest.mark.asyncio
# async def test_update_contact(contact_repository, mock_session, user):
#     # Setup
#     contact_data = ContactBase(
#         last_name="Skywalker"
#     )
#     existing_contact = Contact(id=1, first_name="Luke", last_name="Oldman", user=user)
#     mock_result = MagicMock()
#     mock_result.scalar_one_or_none.return_value = existing_contact
#     mock_session.execute = AsyncMock(return_value=mock_result)
#
#     # Call method
#     result = await contact_repository.update_contact(contact_id=1, body=contact_data, user=user)
#
#     # Assertions
#     assert result is not None
#     assert result.first_name == "Luke"
#     assert result.last_name == "Skywalker"
#     mock_session.commit.assert_awaited_once()
#     mock_session.refresh.assert_awaited_once_with(existing_contact)
#
# @pytest.mark.asyncio
# async def test_remove_contact(contact_repository, mock_session, user):
#     # Setup
#     existing_contact = Contact(id=1, first_name="Luke", last_name="Oldman", user=user)
#     mock_result = MagicMock()
#     mock_result.scalar_one_or_none.return_value = existing_contact
#     mock_session.execute = AsyncMock(return_value=mock_result)
#
#     # Call method
#     result = await contact_repository.remove_contact(contact_id=1, user=user)
#
#     # Assertions
#     assert result is not None
#     assert result.last_name == "Oldman"
#     mock_session.delete.assert_awaited_once_with(existing_contact)
#     mock_session.commit.assert_awaited_once()
#
