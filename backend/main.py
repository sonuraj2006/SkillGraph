from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import test_connection
from routes.students import router as students_router
from routes.recommendations import router as recommendations_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students_router)
app.include_router(recommendations_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SkillGraph"
    }


@app.get("/health")
def health():
    try:
        message = test_connection()

        return {
            "status": "connected",
            "database": "CognoDB",
            "message": message
        }

    except Exception:
        return {
            "status": "error",
            "database": "CognoDB",
            "message": "Unable to connect to database"
        }