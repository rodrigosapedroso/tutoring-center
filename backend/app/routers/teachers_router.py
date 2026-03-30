import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Teacher, UserRole
from ..schemas import TeacherCreate, TeacherRead
from ..auth import require_admin
from ..utils.password import generate_password, hash_password

router = APIRouter(prefix="/api/teachers")

@router.post("/", response_model=TeacherRead, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher_data: TeacherCreate, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == teacher_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

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

    return teacher
