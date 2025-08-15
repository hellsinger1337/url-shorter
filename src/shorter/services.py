from fastapi import HTTPException, status
from pydantic import AnyUrl
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud
from .utils import generate_code


class UrlShortenerService:
    def __init__(self, db: Session):
        self.db = db

    def create_short_url(self, original_url: AnyUrl) -> str:
        for _ in range(10):
            code = generate_code(6)
            try:
                crud.create_mapping(self.db, code=code, original_url=str(original_url))
                return code
            except IntegrityError:
                self.db.rollback()
                continue
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate unique code",
        )

    def resolve_and_count(self, code: str) -> str:
        m = crud.get_by_code(self.db, code)
        if not m:
            raise HTTPException(status_code=404, detail="Code not found")
        crud.increment_clicks(self.db, code)
        return m.original_url

    def get_stats(self, code: str):
        m = crud.get_by_code(self.db, code)
        if not m:
            raise HTTPException(status_code=404, detail="Code not found")
        return m
