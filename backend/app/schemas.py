from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from .models import (
    ClassFrequencyType,
    ClassType,
    DisciplineLevel,
    EvaluationScore,
    UserRole,
)


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserRead(UserBase, ORMBase):
    id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


#for token response
class Token(BaseModel):
    access_token: str
    token_type: str


class ParentBase(BaseModel):
    name: str
    contact: str
    address: str
    email: EmailStr


class ParentCreate(ParentBase):
    user_id: Optional[str]


class ParentRead(ParentBase, ORMBase):
    id: str
    user_id: Optional[str]


class ParentUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None


# For parent list read operations
class ParentList(ORMBase):
    id: str
    name: str
    contact: str
    email: EmailStr
    students_count: int


class StudentBase(BaseModel):
    name: str
    birth: date
    nationality: str
    contact: Optional[str]


class StudentCreate(StudentBase):
    parent_ids: Optional[List[str]] = []


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    birth: Optional[date] = None
    nationality: Optional[str] = None
    contact: Optional[str] = None
    parent_ids: Optional[List[str]] = None


# For student detail read operations
class StudentRead(StudentBase, ORMBase):
    id: str
    parents: List[ParentRead]
    classes: List[str]  


# For student list read operations
class StudentList(ORMBase):
    id: str
    name: str
    levels: List[DisciplineLevel]
    disciplines: List[str]
    teachers: Optional[List[str]]


class DisciplineBase(BaseModel):
    name: str
    level: DisciplineLevel


class DisciplineCreate(DisciplineBase):
    pass


class DisciplineRead(DisciplineBase, ORMBase):
    id: int


class TeacherBase(BaseModel):
    name: str
    birth: date
    nationality: str
    contact: str
    email: EmailStr


class TeacherCreate(TeacherBase):
    discipline_ids: list[int]


class TeacherRead(TeacherBase, ORMBase):
    id: str
    user_id: Optional[str]
    disciplines: list[DisciplineRead]


# For teacher update
class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    birth: Optional[date] = None
    nationality: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[EmailStr] = None
    discipline_ids: Optional[list[int]] = None


#For teacher list read operations
class TeacherList(ORMBase):
    id: str
    name: str
    levels: List[DisciplineLevel]
    disciplines: List[str]


class ClassBase(BaseModel):
    teacher_id: str
    discipline_id: int
    student_ids: List[str]
    level: DisciplineLevel
    type: ClassType


class ClassCreate(ClassBase):
    pass


class ClassRead(ClassBase, ORMBase):
    id: str
    students: List[StudentRead]
    teacher: TeacherRead
    discipline: DisciplineRead


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


class ClassScheduleRead(ClassScheduleBase, ORMBase):
    id: int


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


class AttendanceRead(AttendanceBase, ORMBase):
    id: int
    date: datetime
    student: StudentRead
    teacher: TeacherRead
    class_: ClassRead


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


class EvaluationRead(EvaluationBase, ORMBase):
    id: int
    student: StudentRead
    teacher: TeacherRead
    discipline: DisciplineRead
