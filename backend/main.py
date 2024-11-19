from fastapi import FastAPI
from backend.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# In your main.py or startup script
from backend.database import engine
from backend.models import Base

# Create all tables
Base.metadata.create_all(bind=engine)

# Serve static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Include routes
app.include_router(router)
