from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.class_service import (
    create_class as create_class_service, 
    get_classes as get_classes_service,
    update_class as update_class_service,
    delete_class as delete_class_service
)
from ..database import get_db
from ..models import User
from ..schemas import ClassCreate, ClassRead, ClassUpdate
from ..auth import get_current_user, require_admin

router = APIRouter(prefix="/api/classes")


@router.post("/", response_model=ClassRead)
def create_class(
    class_data: ClassCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    new_class = create_class_service(class_data, db)
    return new_class


@router.get("/", response_model=list[ClassRead])
def get_classes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_classes_service(current_user, db)


@router.patch("/{class_id}", response_model=ClassRead)
def update_class(
    class_id: str,
    data: ClassUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    return update_class_service(class_id, data, db)


@router.delete("/{class_id}")
def delete_class(
    class_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    class_ = delete_class_service(class_id, db)
    return class_
