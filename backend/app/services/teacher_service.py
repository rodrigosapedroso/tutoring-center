import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import TeacherCreate, TeacherUpdate
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

def get_teachers(db: Session):
    """
    Get all teachers with their name, levels, and disciplines.
    Only called by admin.
    """
    teachers = db.query(Teacher).filter(Teacher.is_active == True).all()
    
    result = []
    for teacher in teachers:
        levels = {d.level for d in teacher.disciplines if d}
        disciplines = {d.name for d in teacher.disciplines if d}
        result.append({
            "id": teacher.id,
            "name": teacher.name,
            "levels": list(levels),
            "disciplines": list(disciplines)
        })
    
    return result


def get_teacher_by_id(teacher_id: str, db: Session):
    """
    Get teacher details by id.
    Only called by admin.
    """
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id,
        Teacher.is_active == True
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    return teacher


def update_teacher(teacher_id: str, teacher_data: TeacherUpdate, db: Session):
    """
    Update teacher data. Only called by admin.
    """
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id,
        Teacher.is_active == True
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    # Update fields if provided
    if teacher_data.name is not None:
        teacher.name = teacher_data.name
    if teacher_data.birth is not None:
        teacher.birth = teacher_data.birth
    if teacher_data.nationality is not None:
        teacher.nationality = teacher_data.nationality
    if teacher_data.contact is not None:
        teacher.contact = teacher_data.contact
    if teacher_data.email is not None:
        teacher.email = teacher_data.email
    
    # Update disciplines if provided
    if teacher_data.discipline_ids is not None:
        disciplines = db.query(Discipline).filter(
            Discipline.id.in_(teacher_data.discipline_ids)
        ).all()
        
        if len(disciplines) != len(teacher_data.discipline_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more disciplines not found"
            )
        
        teacher.disciplines = disciplines
    
    db.commit()
    db.refresh(teacher)
    
    return teacher


def delete_teacher(teacher_id: str, db: Session):
    """
    Delete teacher (soft delete - mark as inactive).
    Only called by admin.
    """
    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id,
        Teacher.is_active == True
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    # Soft delete
    teacher.is_active = False
    db.commit()
    
    return {"detail": f"Teacher {teacher_id} deleted successfully"}
