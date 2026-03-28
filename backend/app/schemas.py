from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from .models import (
    ClassFrequencyType,
    ClassType,
    DisciplineLevel,
    EvaluationScore,
    UserRole,
)

# --- Base Schemas ---

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str

    class Config:
        orm_mode = True


class ParentBase(BaseModel):
    name: str
    contact: str
    address: str
    email: EmailStr


class ParentCreate(ParentBase):
    user_id: Optional[str]


class ParentRead(ParentBase):
    id: str
    user_id: Optional[str]

    class Config:
        orm_mode = True


class TeacherBase(BaseModel):
    name: str
    birth: date
    nationality: str
    contact: str
    email: EmailStr


class TeacherCreate(TeacherBase):
    user_id: Optional[str]


class TeacherRead(TeacherBase):
    id: str
    user_id: Optional[str]

    class Config:
        orm_mode = True


class StudentBase(BaseModel):
    name: str
    birth: date
    nationality: str
    contact: Optional[str]


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: str
    parents: List[ParentRead]
    classes: List[str]

    class Config:
        orm_mode = True


class DisciplineBase(BaseModel):
    name: str
    level: DisciplineLevel


class DisciplineCreate(DisciplineBase):
    pass


class DisciplineRead(DisciplineBase):
    id: int

    class Config:
        orm_mode = True


class ClassBase(BaseModel):
    teacher_id: str
    discipline_id: int
    student_ids: List[str]
    level: DisciplineLevel
    type: ClassType


class ClassCreate(ClassBase):
    pass


class ClassRead(ClassBase):
    id: str
    students: List[StudentRead]
    teacher: TeacherRead
    discipline: DisciplineRead

    class Config:
        orm_mode = True


class ClassScheduleBase(BaseModel):
    class_id: str
    weekday: int
    time: str
    duration: int
    frequency: ClassFrequencyType
    start_date: date
    end_date: Optional[date]


class ClassScheduleCreate(ClassScheduleBase):
    pass


class ClassScheduleRead(ClassScheduleBase):
    id: int

    class Config:
        orm_mode = True


class AttendanceBase(BaseModel):
    class_id: str
    student_id: str
    teacher_id: str
    discipline_id: int

    present: bool

    contents: Optional[str]
    homework: Optional[str]
    observations: Optional[str]

    teacher_signature: str
    student_signature: Optional[str]

    absence_reason: Optional[str]
    notified_at: Optional[datetime]
    makeup_date: Optional[date]


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: int
    date: datetime
    student: StudentRead
    teacher: TeacherRead
    class_: ClassRead

    class Config:
        orm_mode = True


class AttendanceSummary(BaseModel):
    student_name: str
    discipline_name: str
    time: str
    present: bool


class EvaluationBase(BaseModel):
    student_id: str
    teacher_id: str
    discipline_id: int
    start_date: date
    end_date: date
    behavior: Optional[str]
    score: EvaluationScore
    strategies: Optional[str]
    teacher_signature: str
    parent_comment: Optional[str]


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationRead(EvaluationBase):
    id: int
    student: StudentRead
    teacher: TeacherRead
    discipline: DisciplineRead

    class Config:
        orm_mode = True
