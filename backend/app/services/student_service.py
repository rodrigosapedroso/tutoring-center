import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session, join
from sqlalchemy import distinct

from ..schemas import StudentCreate
from ..models import Student, Parent, Teacher, User, UserRole, Class


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


def get_students(user_id: str, user_role: UserRole, db: Session):
    """
    Get students based on user role with structured data:
    - ADMIN: returns all students with name, levels, disciplines, teachers
    - TEACHER: returns students from teacher's classes with name, levels, disciplines
    """

    if user_role == UserRole.ADMIN:
        # Admin can see all students with teachers
        students = db.query(Student).filter(Student.is_active == True).all()
        
        # Return structured data with teachers
        student_columns = []
        for student in students:
            levels = {c.discipline.level for c in student.classes if c.discipline}
            disciplines = {c.discipline.name for c in student.classes if c.discipline}
            teachers = {c.teacher.name for c in student.classes if c.teacher}
            student_columns.append({
                "id": student.id,
                "name": student.name,
                "levels": levels,
                "disciplines": disciplines,
                "teachers": teachers
            })
        
        return student_columns
    
    elif user_role == UserRole.TEACHER:
        # Get teacher and their students through classes
        teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        # Get all students from teacher's classes
        students = db.query(Student).join(Student.classes).filter(
            Class.teacher_id == teacher.id,
            Student.is_active == True
        ).distinct().all()
        
        # Return structured data without teachers
        student_columns = []
        for student in students:
            levels = {c.discipline.level for c in student.classes if c.discipline}
            disciplines = {c.discipline.name for c in student.classes if c.discipline}
            student_columns.append({
                "id": student.id,
                "name": student.name,
                "levels": list(levels),
                "disciplines": list(disciplines),
            })
        
        return student_columns
    
    else:
        raise HTTPException(status_code=400, detail="Invalid user role")
