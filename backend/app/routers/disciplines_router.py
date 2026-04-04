from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services.discipline_service import create_discipline
from ..database import get_db
from ..models import Discipline, User
from ..schemas import DisciplineCreate, DisciplineRead
from ..auth import require_admin

router = APIRouter(prefix="/api/discipline")

@router.post("/", response_model=DisciplineRead)
def create_discipline_endpoint(
    data: DisciplineCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin)
):  
    return create_discipline(data, db)
    

@router.get("/", response_model=list[DisciplineRead])
def get_disciplines(db: Session = Depends(get_db)):
    disciplines = db.query(Discipline).all()
    return disciplines