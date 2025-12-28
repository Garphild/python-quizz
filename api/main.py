from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.home import router as home_router

from routes.admin.quizz.quizz import admin_quizz_router
from routes.admin.quizz.answers import admin_answers_router
from routes.admin.quizz.ai import admin_ai_router

from routes.auth.email import router as email_router
from routes.auth.google import router as google_router

from routes.quizz.quizz import router as quizz_router
from routes.quizz.answers import router as answers_router

app = FastAPI(
    title="Quizz API",
    description="Backend API for the Quizz application",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------ Home routes --------------------------
app.include_router(home_router)
app.include_router(health_router)

# ------------ Admin routes -------------------------
app.include_router(admin_quizz_router)
app.include_router(admin_answers_router)

# ------------ Admin AI routes ----------------------
app.include_router(admin_ai_router)

# ------------ Auth routes --------------------------
app.include_router(email_router)
app.include_router(google_router)

# ------------ Quizz routes -------------------------
app.include_router(quizz_router)
app.include_router(answers_router)
