"""
Utils File for Data Generation
"""

import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Doctors, Patients, Provinces, Admissions


class DataGenerator:

    @staticmethod
    async def init_db():
        """check database tables and entries"""
        db = next(get_db())
        check_doctor = db.query(Doctors).all()
        if check_doctor is None or len(check_doctor) == 0:
            await DataGenerator.create_doctor_entries(db=db)
        check_province = db.query(Provinces).all()
        if check_province is None or len(check_province) == 0:
            await DataGenerator.create_provinces_entries(db=db)
        check_patients = db.query(Patients).all()
        if check_patients is None or len(check_patients) == 0:
            await DataGenerator.create_patients_entries(db=db)
        check_admission = db.query(Admissions).all()
        if check_admission is None or len(check_admission) == 0:
            DataGenerator.create_admissions_entires(db=db)

    @staticmethod
    async def destroy_db():
        """collapse the db of entries"""
        pass

    @staticmethod
    async def create_doctor_entries(db: Session):
        """creates entries in doctor"""
        faker = Faker()
        obj_list = []
        speciality = [
            "Internist",
            "Cardiologist",
            "General Surgeon",
            "Obstetrician/Gynecologist",
            "Gastroenterologist",
            "Psychiatrist",
            "Oncologist",
            "Pediatrician",
            "Neurologist",
            "Orthopaedic Surgeon",
            "Respirologist",
            "Cardiovascular Surgeon",
            "Nuclear Medicine",
            "Gerontologist",
            "Urologist",
        ]
        for speci in speciality:
            name = faker.name().split(" ")
            obj_list.append(
                Doctors(
                    first_name=name[0], last_name=name[1], speciality=speci
                )
            )
        db.add_all(obj_list)
        db.commit()

    @staticmethod
    async def create_provinces_entries(db: Session):
        """creates provinces entries"""
        provinces = {
            "AB": "Alberta",
            "BC": "British Columbia",
            "MB": "Manitoba",
            "NB": "New Brunswick",
            "NL": "Newfoundland and Labrador",
            "NT": "Northwest Territories",
            "NS": "Nova Scotia",
            "NU": "Nunavut",
            "ON": "Ontario",
            "PE": "Prince Edward Island",
            "QC": "Quebec",
            "SK": "Saskatchewan",
            "YT": "Yukon",
        }
        obj_list = [
            Provinces(provience_id=key, province_name=value)
            for key, value in provinces.items()
        ]
        db.add_all(obj_list)
        db.commit()

    @staticmethod
    async def create_patients_entries(db: Session):
        """create patient entires"""
        faker = Faker()
        obj_list = []
        for _ in range(0, 5000):
            name = faker.name().split(" ")
            obj_list.append(
                Patients(
                    first_name=name[0],
                    last_name=name[1],
                    gender=random.choice(["M", "F"]),
                    birth_date=faker.date_of_birth(),
                    city=faker.city(),
                    province_id=random.choice(
                        [
                            "AB",
                            "BC",
                            "MB",
                            "NB",
                            "NL",
                            "NT",
                            "NS",
                            "NU",
                            "ON",
                            "PE",
                            "QC",
                            "SK",
                            "YT",
                        ]
                    ),
                    allergies=random.choice(
                        [
                            None,
                            "Penicillin",
                            "Aspirin",
                            "Ibuprofen",
                            "Codeine",
                            "Sulfonamides",
                            "Erythromycin",
                            "Shellfish",
                            "Peanuts",
                            "Tree nuts",
                            "Eggs",
                            "Milk",
                            "Soy",
                            "Wheat",
                            "Latex",
                            "Dust mites",
                            "Mold",
                            "Pet dander",
                            "Insect stings",
                            "Pollens",
                            "Nickel",
                            "Sunlight",
                            "Lactose",
                            "Gluten",
                            "Fish",
                            "Cockroach",
                            "Chlorine",
                            "Insect repellents",
                            "Cold",
                            "Heat",
                            "Soy sauce",
                            "Dairy products",
                            "Eggs",
                            "Sesame seeds",
                            "Cats",
                            "Dogs",
                            "Horses",
                            "Rabbits",
                            "Rodents",
                            "Insect venom",
                            "Formaldehyde",
                            "Pollen",
                            "Nickel",
                            "Medications",
                            "Chemicals",
                            "Metals",
                            "Fruits",
                            "Vegetables",
                        ]
                    ),
                    height=round(random.uniform(50.50, 180.50), 2),
                    weight=round(random.uniform(50.50, 110.50), 2),
                )
            )
        db.add_all(obj_list)
        db.commit()

    @staticmethod
    def create_admissions_entires(db: Session):
        """create admission entries"""
        faker = Faker()
        patients_id_list = db.query(Patients.patient_id).all()
        attending_doctor_id_list = db.query(Doctors.doctor_id).all()
        obj_list = []
        for _ in range(0, 9000):
            admission_date = datetime.strptime(faker.date(), "%Y-%m-%d")
            discharge_date = admission_date + timedelta(
                days=random.randrange(15)
            )
            obj_list.append(
                Admissions(
                    patient_id=random.choice(patients_id_list)[0],
                    admission_date=admission_date,
                    discharge_date=discharge_date,
                    diagnosis=faker.text(),
                    attending_doctor_id=random.choice(
                        attending_doctor_id_list
                    )[0],
                )
            )
        db.add_all(obj_list)
        db.commit()
