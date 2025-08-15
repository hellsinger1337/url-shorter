from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from .config import settings
from .db import init_db, session_scope
from .schemas import ShortenRequest, ShortenResponse, StatsResponse
from .services import UrlShortenerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="URL Shortener", version="1.0.0", lifespan=lifespan)


def get_db():
    with session_scope() as db:
        yield db


def get_service(db: Annotated[Session, Depends(get_db)]) -> UrlShortenerService:
    return UrlShortenerService(db)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid input format", "errors": exc.errors()},
    )


@app.post("/api/v1/shorten", response_model=ShortenResponse)
def shorten(
    payload: ShortenRequest,
    request: Request,
    svc: Annotated[UrlShortenerService, Depends(get_service)],
):
    code = svc.create_short_url(payload.url)
    base = settings.BASE_URL or str(request.base_url).rstrip("/")
    short_url = f"{base}/s/{code}"
    return ShortenResponse(code=code, short_url=short_url)


@app.get("/s/{code}")
def redirect(code: str, svc: Annotated[UrlShortenerService, Depends(get_service)]):
    target = svc.resolve_and_count(code)
    return RedirectResponse(url=target, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/api/v1/stats/{code}", response_model=StatsResponse)
def stats(code: str, svc: Annotated[UrlShortenerService, Depends(get_service)]):
    m = svc.get_stats(code)
    return StatsResponse(
        code=m.code,
        original_url=m.original_url,
        clicks=m.clicks,
        created_at=m.created_at,
    )
