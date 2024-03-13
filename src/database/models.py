"""
Models for SqlAlchemy
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Numeric,
    Date,
    Text,
)
from database.db import Base


class TableName:
    hospital: list = [
        "doctors",
        "patients",
        "admissions",
        "provinces_names",
        "doctors;",
        "patients;",
        "admissions;",
        "provinces_names;",
    ]


class Doctors(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    speciality = Column(String(25))


class Provinces(Base):
    __tablename__ = "provinces_names"

    province_id = Column(String(2), primary_key=True)
    province_name = Column(String(30))


class Patients(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    gender = Column(String(1))
    birth_date = Column(Date)
    city = Column(String(30))
    province_id = Column(String(2), ForeignKey("provinces_names.provience_id"))
    allergies = Column(String(80))
    height = Column(Numeric(2))
    weight = Column(Numeric(2))


class Admissions(Base):
    __tablename__ = "admissions"

    admissions_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    admission_date = Column(Date)
    discharge_date = Column(Date)
    diagnosis = Column(String(50))
    attending_doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))


class Questions(Base):
    __tablename__ = "sql_questions"

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    difficulty = Column(Text)
    hints = Column(String)
    tags = Column(String)
