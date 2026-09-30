from pydantic import BaseModel
from datetime import date, time


class PatientBase(BaseModel):
    username: str
    email: str
    password: str


class PatientDisplay(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class DoctorBase(BaseModel):
    username: str
    specialization: str
    email: str
    password: str


class AvailabilityBase(BaseModel):
    doctor_id: int
    date: date


class AvailabilityDisplay(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

class DoctorBasicDisplay(BaseModel):
    username: str
    specialization: str
    email: str

    class Config:
        from_attributes = True

class DoctorDisplay(BaseModel):
    username: str
    specialization: str
    email: str
    availabilities: list[AvailabilityDisplay]

    class Config:
        from_attributes = True


class AdminBase(BaseModel):
    username: str
    email: str
    password: str


class AdminDisplay(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    patient_id: int
    availability_id: int


class AppointmentDisplay(BaseModel):
    id: int
    patient_id: int
    doctor_username: str
    date: date
    start_time: time
    end_time: time
    status: str

    class Config:
        from_attributes = True


class Auth(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True