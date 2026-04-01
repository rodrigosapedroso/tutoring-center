from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.teacher_service import create_teacher
from ..database import get_db
from ..models import User
from ..schemas import TeacherCreate, TeacherRead
from ..auth import require_admin

router = APIRouter(prefix="/api/teachers")

@router.post("/", response_model=TeacherRead)
def create_teacher_endpoint(
    teacher_data: TeacherCreate, 
    db: Session = Depends(get_db), 
    _: User = Depends(require_admin)
):
    try:
        teacher = create_teacher(teacher_data, db)
        return teacher
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))