import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, join
from sqlalchemy import distinct

from ..schemas import StudentCreate, StudentUpdate
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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="One or more parents not found"
            )

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
                "levels": list(levels),
                "disciplines": list(disciplines),
                "teachers": list(teachers)
            })
        
        return student_columns
    
    elif user_role == UserRole.TEACHER:
        # Get teacher and their students through classes
        teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Teacher not found"
            )
        
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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to view students"
        )
    
def get_student_by_id(student_id: str, user: User, db: Session):
    """
    Get student by ID with access control:
    - ADMIN: can view any student
    - TEACHER: can view students in their classes
    - PARENT: can view their own children
    """
    student = db.query(Student).filter(
        Student.id == student_id, 
        Student.is_active == True
    ).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if user has access to this student
    if user.role == UserRole.ADMIN:
        return student
    elif user.role == UserRole.TEACHER:
        teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )
        # Check if teacher has a class with this student
        has_access = db.query(Class).join(Class.students).filter(
            Class.teacher_id == teacher.id,
            Student.id == student_id
        ).first()
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to view this student"
            )
        return student
    elif user.role == UserRole.PARENT:
        parent = db.query(Parent).filter(Parent.user_id == user.id).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent not found"
            )
        # Check if parent is associated with this student
        if student not in parent.students:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed to view this student"
            )
        return student
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to view students"
        )


def update_student(student_id: str, student_data: StudentUpdate, db: Session):
    """
    Update student data. Only called by admin.
    """
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.is_active == True
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Update fields if provided
    if student_data.name is not None:
        student.name = student_data.name
    if student_data.birth is not None:
        student.birth = student_data.birth
    if student_data.nationality is not None:
        student.nationality = student_data.nationality
    if student_data.contact is not None:
        student.contact = student_data.contact
    
    # Update parents if provided
    if student_data.parent_ids is not None:
        parents = db.query(Parent).filter(
            Parent.id.in_(student_data.parent_ids)
        ).all()
        
        if len(parents) != len(student_data.parent_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or more parents not found"
            )
        
        student.parents = parents
    
    db.commit()
    db.refresh(student)
    
    return student


def delete_student(student_id: str, db: Session):
    """
    Delete student (soft delete - mark as inactive).
    Only called by admin.
    """
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.is_active == True
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Soft delete
    student.is_active = False
    db.commit()
    
    return {"detail": f"Student {student_id} deleted successfully"}
