from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db.database import engine
from db.models import base
from routers import patient , doctors , admin , availability , appointment
from auth import authentication

app = FastAPI()
app.include_router(patient.router)
app.include_router(doctors.router)
app.include_router(admin.router)
app.include_router(availability.router)
app.include_router(appointment.router)
app.include_router(authentication.router)

base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return 'first page'