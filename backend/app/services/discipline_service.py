from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from ..schemas import DisciplineCreate
from ..models import Discipline

def create_discipline(data: DisciplineCreate, db: Session):
    existing = db.query(Discipline).filter(
        Discipline.name == data.name,
        Discipline.level == data.level
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discipline already exists with the same name and level"
        )

    discipline = Discipline(
        name=data.name,
        level=data.level
    )

    db.add(discipline)
    db.commit()
    db.refresh(discipline)

    return discipline