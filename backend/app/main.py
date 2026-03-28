#File to create the app FastAPI, import routes and connect them to the app
from fastapi import FastAPI
from . import models
from app.database import Base, engine

app = FastAPI(title="Tutoring Center")

@app.get("/") 
async def root(): 
    return {
        "status": "ok",
        "service": "Tutoring Center API"
    }

# Create database tables
Base.metadata.create_all(bind=engine)
