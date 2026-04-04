import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import TeacherCreate
from .email_service import send_email
from ..models import User, UserRole, Teacher, Discipline
from ..utils.hashing import generate_password, hash_password


def create_teacher(teacher_data: TeacherCreate, db: Session):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == teacher_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

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
    db.flush()

    disciplines = db.query(Discipline).filter(
        Discipline.id.in_(teacher_data.discipline_ids)
    ).all()

    if len(disciplines) != len(teacher_data.discipline_ids):
        raise ValueError("One or more disciplines not found")
    
    # Create teacher profile
    teacher = Teacher(
        id=str(uuid.uuid4()),
        user_id=user.id,
        name=teacher_data.name, 
        birth=teacher_data.birth,
        nationality=teacher_data.nationality,
        contact=teacher_data.contact,
        email=teacher_data.email,
        disciplines=disciplines
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    try:
        send_email(
            to_email=teacher_data.email, 
            name=teacher_data.name, 
            temporary_password=raw_password
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )

    return teacher