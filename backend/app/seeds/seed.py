#file to insert disciplines into the database
from ..models import Discipline
from ..database import SessionLocal
from .discipline_list import DISCIPLINES as disciplines

def seed_disciplines():
    db = SessionLocal()

    for level, names in disciplines.items():
        for name in names:
            existing = db.query(Discipline).filter(
                Discipline.name == name,
                Discipline.level == level
            ).first()

            if not existing:
                new_disc = Discipline(name=name, level=level)
                db.add(new_disc)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_disciplines()