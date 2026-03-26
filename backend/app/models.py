import enum
from .database import Base
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum, Text, LargeBinary, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


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
    parents = relationship("Parent", secondary=lambda: student_parents, back_populates="students")
    teachers = relationship("Teacher", secondary=lambda: student_teachers, back_populates="students")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Relationships 
    user = relationship("User", back_populates="parent")
    students = relationship("Student", secondary="student_parents", back_populates="parents")


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
    students = relationship("Student", secondary="student_teachers", back_populates="teachers")


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

# Enum for education levels
class EducationLevel(enum.Enum):
    BASIC = "basic"
    SECONDARY = "secondary"
    HIGHER = "higher"


class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Enum(EducationLevel))





    