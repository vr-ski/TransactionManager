from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_router import router as auth_router
from app.api.contractor_router import router as contractor_router
from app.api.health_router import router as health_router
from app.api.status_router import router as status_router
from app.api.transaction_router import router as transaction_router
from app.api.transaction_type_router import router as transaction_type_router
from app.api.user_router import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Payments API",
        version="1.0.0",
        description="Clean architecture backend for contractor payments",
    )

    # -----------------------------
    # CORS (optional but recommended)
    # -----------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # adjust for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -----------------------------
    # Routers
    # -----------------------------
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(transaction_router)
    app.include_router(contractor_router)
    app.include_router(status_router)
    app.include_router(transaction_type_router)
    app.include_router(health_router)

    return app


app = create_app()
