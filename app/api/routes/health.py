from fastapi import APIRouter

from app.application.use_cases.get_status import get_status_use_case

router = APIRouter()


@router.get("/api/status")
def get_status():
    return get_status_use_case()