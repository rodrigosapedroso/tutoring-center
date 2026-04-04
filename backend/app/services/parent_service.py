import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import ParentCreate
from .email_service import send_email
from ..models import User, UserRole, Parent
from ..utils.hashing import generate_password, hash_password


def create_parent(parent_data: ParentCreate, db: Session):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == parent_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    raw_password = generate_password()
    hashed_password = hash_password(raw_password)

    # Create user account for parent
    user = User(
        id=str(uuid.uuid4()),
        email=parent_data.email,
        password_hash=hashed_password,
        role=UserRole.PARENT
    )
    db.add(user)
    db.flush()

    # Create parent profile
    parent = Parent(
        id=str(uuid.uuid4()),
        user_id=user.id,
        name=parent_data.name,
        contact=parent_data.contact,
        address=parent_data.address,
        email=parent_data.email,
    )
    db.add(parent)
    db.commit()
    db.refresh(parent)

    try:
        send_email(
            to_email=parent_data.email,
            name=parent_data.name,
            temporary_password=raw_password
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )

    return parent
