#File to create the app FastAPI, import routes and connect them to the app
from fastapi import FastAPI
from .database import Base, engine
from .routers import auth_router
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