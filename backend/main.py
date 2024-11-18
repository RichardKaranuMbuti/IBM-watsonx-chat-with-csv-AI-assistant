from fastapi import FastAPI
from backend.routes import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Include routes
app.include_router(router)
