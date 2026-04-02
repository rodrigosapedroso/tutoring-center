import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..schemas import StudentCreate
from ..models import Student, Parent


def create_student(student_data: StudentCreate, db: Session):
    # Create student profile
    student = Student(
        id=str(uuid.uuid4()),
        name=student_data.name,
        birth=student_data.birth,
        nationality=student_data.nationality,
        contact=student_data.contact,
    )

    # Associate parents (if given)
    if student_data.parent_ids:
        parents = db.query(Parent).filter(
            Parent.id.in_(student_data.parent_ids)
        ).all()

        if len(parents) != len(student_data.parent_ids):
            raise HTTPException(status_code=404, detail="One or more parents not found")

        student.parents = parents

    db.add(student)
    db.commit()
    db.refresh(student)
    
    return student
