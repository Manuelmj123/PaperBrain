from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.infrastructure.ui.html_page import ui_html

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=ui_html())