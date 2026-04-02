from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..services.parent_service import create_parent
from ..database import get_db
from ..models import User
from ..schemas import ParentCreate, ParentRead
from ..auth import require_admin

router = APIRouter(prefix="/api/parents")

@router.post("/", response_model=ParentRead)
def create_parent_endpoint(
    parent_data: ParentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):
    try:
        parent = create_parent(parent_data, db)
        return parent
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
