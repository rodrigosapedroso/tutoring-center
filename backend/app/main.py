#File to create the app FastAPI, import routes and connect them to the app
from dotenv import load_dotenv

# Load .env variables into environment
load_dotenv()

from fastapi import FastAPI
from .database import Base, engine
from .routers import (
    auth_router, 
    disciplines_router, 
    teachers_router, 
    students_router, 
    parents_router, 
    class_router
)
from . import models

app = FastAPI(title="Tutoring Center")

@app.get("/") 
async def root(): 
    return {
        "status": "ok",
        "service": "Tutoring Center API"
    }

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router.router)
app.include_router(disciplines_router.router)
app.include_router(teachers_router.router)
app.include_router(students_router.router)
app.include_router(parents_router.router)
app.include_router(class_router.router)