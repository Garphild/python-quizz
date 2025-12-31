from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.home import router as home_router

from routes.auth import authRouter
from routes.answers import answer_router
from routes.questions import question_router
from routes.quizz import quizz_router

from core.lifespan import lifespan

app = FastAPI(
    title="Quizz API",
    description="Backend API for the Quizz application",
    version="0.1.0",
    lifespan=lifespan
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

# ------------ Auth routes --------------------------
app.include_router(authRouter)

# ------------ Quizz routes -------------------------
app.include_router(quizz_router)

# ------------ Question routes ----------------------
app.include_router(question_router)

# ------------ Answer routes ------------------------
app.include_router(answer_router)