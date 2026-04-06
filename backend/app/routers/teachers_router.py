from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.teacher_service import (
    create_teacher, 
    get_teachers as get_teachers_service,
    get_teacher_by_id as get_teacher_by_id_service,
    update_teacher as update_teacher_service,
    delete_teacher as delete_teacher_service
)
from ..database import get_db
from ..models import User
from ..schemas import TeacherCreate, TeacherList, TeacherRead, TeacherUpdate
from ..auth import require_admin

router = APIRouter(prefix="/api/teachers")

@router.post("/", response_model=TeacherRead)
def create_teacher_endpoint(
    teacher_data: TeacherCreate, 
    db: Session = Depends(get_db), 
    _: User = Depends(require_admin)
):
    teacher = create_teacher(teacher_data, db)
    return teacher


@router.get("/", response_model=list[TeacherList])
def get_teachers(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    teachers = get_teachers_service(db)
    return teachers


@router.get("/{teacher_id}", response_model=TeacherRead)
def get_teacher_by_id(
    teacher_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    teacher = get_teacher_by_id_service(teacher_id, db)
    return teacher


@router.patch("/{teacher_id}", response_model=TeacherRead)
def update_teacher(
    teacher_id: str,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    teacher = update_teacher_service(teacher_id, teacher_data, db)
    return teacher


@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    teacher = delete_teacher_service(teacher_id, db)
    return teacher
