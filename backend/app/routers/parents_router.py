from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.parent_service import (
    create_parent,
    get_parents as get_parents_service,
    update_parent as update_parent_service,
    delete_parent as delete_parent_service
)
from ..database import get_db
from ..models import User
from ..schemas import ParentCreate, ParentList, ParentRead, ParentUpdate
from ..auth import require_admin

router = APIRouter(prefix="/api/parents")

@router.post("/", response_model=ParentRead)
def create_parent_endpoint(
    parent_data: ParentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    parent = create_parent(parent_data, db)
    return parent


@router.get("/", response_model=list[ParentList])
def get_parents(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    parents = get_parents_service(db)
    return parents


@router.patch("/{parent_id}", response_model=ParentRead)
def update_parent(
    parent_id: str,
    parent_data: ParentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    parent = update_parent_service(parent_id, parent_data, db)
    return parent


@router.delete("/{parent_id}")
def delete_parent(
    parent_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    parent = delete_parent_service(parent_id, db)
    return parent
