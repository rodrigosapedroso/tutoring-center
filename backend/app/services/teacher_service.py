import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from .email_service import send_email
from ..models import User, UserRole, Teacher
from ..utils.hashing import generate_password, hash_password


def create_teacher(teacher_data, db: Session):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == teacher_data.email).first()
    if existing_user:
        raise ValueError("Email already registered")

    raw_password = generate_password()
    hashed_password = hash_password(raw_password)
    
     # Create user account for teacher
    user = User(
        id=str(uuid.uuid4()),
        email=teacher_data.email, 
        password_hash=hashed_password, 
        role=UserRole.TEACHER
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create teacher profile
    teacher = Teacher(
        id=str(uuid.uuid4()),
        user_id=user.id,
        name=teacher_data.name, 
        birth=teacher_data.birth,
        nationality=teacher_data.nationality,
        contact=teacher_data.contact,
        email=teacher_data.email
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    send_email(to_email=teacher_data.email, name=teacher_data.name, temporary_password=raw_password)

    return teacher