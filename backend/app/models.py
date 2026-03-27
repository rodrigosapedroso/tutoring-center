import enum
from .database import Base
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum, Text, LargeBinary, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# Association tables for many-to-many relationships
student_parents = Table(
    "student_parents",
    Base.metadata,
    Column("student_id", String, ForeignKey("students.id"), primary_key=True),
    Column("parent_id", String, ForeignKey("parents.id"), primary_key=True),
)

student_teachers = Table(
    "student_teachers",
    Base.metadata,
    Column("student_id", String, ForeignKey("students.id"), primary_key=True),
    Column("teacher_id", String, ForeignKey("teachers.id"), primary_key=True),
)

teacher_disciplines = Table(
    "teacher_disciplines",
    Base.metadata,
    Column("teacher_id", String, ForeignKey("teachers.id"), primary_key=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id"), primary_key=True),
)

class_students = Table(
    "class_students",
    Base.metadata,
    Column("class_id", String, ForeignKey("classes.id"), primary_key=True),
    Column("student_id", String, ForeignKey("students.id"), primary_key=True),
)

# Enum for user roles
class UserRole(enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    PARENT = "parent"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    # Relationships
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    parent = relationship("Parent", back_populates="user", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth = Column(Date, nullable=False)
    nationality = Column(String, nullable=False)

    # Relationships 
    parents = relationship("Parent", secondary=student_parents, back_populates="students")
    teachers = relationship("Teacher", secondary=student_teachers, back_populates="students")
    classes = relationship("Class", secondary=class_students, back_populates="students")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Relationships 
    user = relationship("User", back_populates="parent")
    students = relationship("Student", secondary=student_parents, back_populates="parents")


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    birth = Column(Date, nullable=False)
    nationality = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Relationships 
    user = relationship("User", back_populates="teacher")
    students = relationship("Student", secondary=student_teachers, back_populates="teachers")
    classes = relationship("Class", back_populates="teacher")
    disciplines = relationship("Discipline", secondary=teacher_disciplines, back_populates="teachers")


# Enum for education levels
class EducationLevel(enum.Enum):
    BASIC = "basic"
    SECONDARY = "secondary"
    HIGHER = "higher"


class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Enum(EducationLevel), nullable=False)

    # Relationships 
    teachers = relationship("Teacher", secondary=teacher_disciplines, back_populates="disciplines")
    classes = relationship("Class", back_populates="discipline")


class ClassType(enum.Enum):
    INDIVIDUAL = "individual"
    GROUP = "group"


class Class(Base):
    __tablename__ = "classes"

    id = Column(String, primary_key=True)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))
    level = Column(Enum(EducationLevel))
    type = Column(Enum(ClassType))

    # Relationships 
    teacher = relationship("Teacher", back_populates="classes")
    discipline = relationship("Discipline", back_populates="classes")
    students = relationship("Student", secondary=class_students, back_populates="classes")
    schedules = relationship("ClassSchedule", back_populates="class_")


class ClassFrequencyType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True)
    class_id = Column(String, ForeignKey("classes.id"))
    weekday = Column(Integer)  # 0-5
    time = Column(String)
    duration = Column(Integer)
    frequency = Column(Enum(ClassFrequencyType))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Relationships
    class_ = relationship("Class", back_populates="schedules") 


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True)
    class_id = Column(String, ForeignKey("classes.id"))
    student_id = Column(String, ForeignKey("students.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))

    date = Column(DateTime, default=func.now())

    present = Column(Boolean)

    contents = Column(Text)
    homework = Column(Text)
    observations = Column(Text)
    teacher_signature = Column(String)
    student_signature = Column(String)

    absence_reason = Column(Text)
    notified_at = Column(DateTime)
    makeup_date = Column(Date)

    # Relationships 
    student = relationship("Student")
    teacher = relationship("Teacher")
    class_ = relationship("Class")


class EvaluationScore(enum.Enum):
    MUCH_WORSE = "much_worse"
    SLIGHTLY_WORSE = "slightly_worse"
    SAME = "same"
    SLIGHTLY_BETTER = "slightly_better"
    MUCH_BETTER = "much_better"


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    student_id = Column(String, ForeignKey("students.id"))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    behavior = Column(Text)
    score = Column(Enum(EvaluationScore))
    strategies = Column(Text)
    teacher_signature = Column(String)
    parent_comment = Column(Text)

    # Relationships 
    student = relationship("Student")
    teacher = relationship("Teacher")
    discipline = relationship("Discipline")





    