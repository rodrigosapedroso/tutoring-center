import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import ClassCreate
from ..models import Class, ClassType, Discipline, Parent, Parent, Student, Teacher, ClassSchedule, User, UserRole


def create_class(class_data: ClassCreate, db: Session):
    """
    Create a class with schedules. Only called by admin.
    Validates:
    - Teacher exists and is active
    - Teacher has the discipline
    - Discipline exists
    - All students exist and are active
    """
    
    # Validate teacher
    teacher = db.query(Teacher).filter(
        Teacher.id == class_data.teacher_id,
        Teacher.is_active == True
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    # Validate discipline
    discipline = db.query(Discipline).filter(
        Discipline.id == class_data.discipline_id
    ).first()
    
    if not discipline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discipline not found"
        )
    
    if class_data.level != discipline.level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discipline does not match level"
        )
    
    # Validate teacher has this discipline
    if discipline not in teacher.disciplines:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher does not teach this discipline"
        )
    
    # Validate all students exist and are active
    students = db.query(Student).filter(
        Student.id.in_(class_data.student_ids),
        Student.is_active == True
    ).all()
    
    if len(students) != len(class_data.student_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more students not found or inactive"
        )
    
    #Validate class type
    if class_data.type == ClassType.INDIVIDUAL and len(students) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Individual class must have exactly one student"
        )
    
    # Create class
    new_class = Class(
        id=str(uuid.uuid4()),
        teacher_id=class_data.teacher_id,
        discipline_id=class_data.discipline_id,
        level=class_data.level,
        type=class_data.type,
        students=students
    )
    
    db.add(new_class)
    db.flush()

     #Validate at least one schedule
    if not class_data.schedules:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class must have at least one schedule"
        )
    
    # Create schedules
    schedules = []
    for schedule_data in class_data.schedules:
        if schedule_data.weekday < 0 or schedule_data.weekday > 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Weekday must be between 0 and 6"
            )
        schedule = ClassSchedule(
            class_id=new_class.id,
            weekday=schedule_data.weekday,
            time=schedule_data.time,
            duration=schedule_data.duration,
            frequency=schedule_data.frequency,
            start_date=schedule_data.start_date,
            end_date=schedule_data.end_date
        )
        schedules.append(schedule)
    
    db.add_all(schedules)
    db.commit()
    db.refresh(new_class)
    
    return new_class

    
def get_classes(user: User, db: Session):

    if user.role == UserRole.ADMIN:
        classes = db.query(Class).all()

    elif user.role == UserRole.TEACHER:
        teacher = db.query(Teacher).filter(
            Teacher.user_id == user.id
        ).first()

        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )

        classes = db.query(Class).filter(
            Class.teacher_id == teacher.id
        ).all()

    elif user.role == UserRole.PARENT:
        parent = db.query(Parent).filter(
            Parent.user_id == user.id
        ).first()

        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent not found"
            )

        student_ids = [s.id for s in parent.students]

        classes = db.query(Class).join(Class.students).filter(
            Student.id.in_(student_ids)
        ).distinct().all()

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed"
        )

    return classes
