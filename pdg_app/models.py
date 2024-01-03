# pdg_app/models.py
import enum
from pdg_app import db
from flask_login import UserMixin


class DepartmentEnum(enum.Enum):
    cardiologie = 0
    maternite = 1
    urgences = 2

def get_department_enum(value):
    try:
        return DepartmentEnum[value]
    except KeyError:
        raise ValueError(f"{value} is not a valid DepartmentEnum")

class Doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    department = db.Column(db.Enum(DepartmentEnum), nullable=False)
    
    def __init__(self, first_name, last_name, email, password, department):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.department = department

    # Méthode requise pour Flask-Login
    def get_id(self):
        return str(self.id)


class PlanningMedecin(db.Model):
    __tablename__ = 'planning_medecin'

    jour = db.Column(db.Integer, primary_key=True)
    id_medecin = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    medecin = db.relationship('Doctor')


class Preference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    day = db.Column(db.Date, nullable=False)
    preference_garde = db.Column(db.Integer, nullable=False)  # 1: dispo, 0: pas arrangeant , -1: indisponible
    preference_astreinte = db.Column(db.Integer, nullable=False)  # 1: dispo, 0: pas arrangeant , -1: indisponible_
