from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.student_service import (
    create_student as create_student_service,
    get_students as get_students_service,
    get_student_by_id as get_student_by_id_service,
    update_student as update_student_service,
    delete_student as delete_student_service,
)
from ..database import get_db
from ..models import User
from ..schemas import StudentCreate, StudentList, StudentRead, StudentUpdate
from ..auth import require_admin, get_current_user

router = APIRouter(prefix="/api/students")

@router.post("/", response_model=StudentRead)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    student = create_student_service(student_data, db)
    return student


@router.get("/", response_model=list[StudentList])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    students = get_students_service(current_user.id, current_user.role, db)
    return students


@router.get("/{student_id}", response_model=StudentRead)
def get_student_by_id(
    student_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_student_by_id_service(student_id, current_user, db)


@router.patch("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: str,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    student = update_student_service(student_id, student_data, db)
    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    return delete_student_service(student_id, db)

