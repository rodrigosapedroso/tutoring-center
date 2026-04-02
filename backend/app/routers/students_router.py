from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.student_service import create_student
from ..database import get_db
from ..models import User
from ..schemas import StudentCreate, StudentRead
from ..auth import require_admin

router = APIRouter(prefix="/api/students")

@router.post("/", response_model=StudentRead)
def create_student_endpoint(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    try:
        student = create_student(student_data, db)
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
