from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.student_service import create_student as create_student_service, get_students as get_students_service
from ..database import get_db
from ..models import User
from ..schemas import StudentCreate, StudentList, StudentRead
from ..auth import require_admin, get_current_user

router = APIRouter(prefix="/api/students")

@router.post("/", response_model=StudentRead)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    try:
        student = create_student_service(student_data, db)
        return student
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[StudentList])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    students = get_students_service(current_user.id, current_user.role, db)
    return students

