from app.api.endpoints import charity_router, donation_router, user_router

from fastapi import APIRouter

main_router = APIRouter()

main_router.include_router(user_router)

main_router.include_router(
    charity_router,
    prefix='/charity_project',
    tags=['charity_project']
)

main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['donation']
)
