"""
Contacts router module
"""

from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactResponse, ContactBase
from src.services.auth import get_current_user
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 20,
    q: str | None = Query(None, max_length=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Retrieve a list of contacts for the authenticated user with optional search.

    Args:
       skip: Number of records to skip.
       limit: Maximum number of records to return.
       q: Optional search query for filtering contacts.
       db: Database session.
       user: The currently authenticated user.

    Returns:
       A list of contact records.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit, user, q)
    return contacts


@router.get("/birthday-reminder", response_model=List[ContactResponse])
async def birthday_reminder(
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    """
    Retrieve a list of contacts with upcoming birthdays.

    Args:
        db: Database session.
        user: The currently authenticated user.

    Returns:
        A list of contacts with upcoming birthdays.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.birthday_reminder(user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Retrieve a specific contact by ID.

    Args:
        contact_id: The ID of the contact to retrieve.
        db: Database session.
        user: The currently authenticated user.

    Returns:
        The contact record if found, otherwise raises an HTTPException.
    """
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactBase,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Create a new contact.

    Args:
        body: The contact details.
        db: Database session.
        user: The currently authenticated user.

    Returns:
        The created contact record.
    """
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_(
    body: ContactBase,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Update an existing contact.

    Args:
        body: The updated contact details.
        contact_id: The ID of the contact to update.
        db: Database session.
        user: The currently authenticated user.

    Returns:
        The updated contact record if found, otherwise raises an HTTPException.
    """
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Remove a contact by ID.

    Args:
        contact_id: The ID of the contact to remove.
        db: Database session.
        user: The currently authenticated user.

    Returns:
        The removed contact record if found, otherwise raises an HTTPException.
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact_by_id(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
