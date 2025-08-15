from sqlalchemy import select, update
from sqlalchemy.orm import Session

from .models import UrlMap


def get_by_code(db: Session, code: str) -> UrlMap | None:
    stmt = select(UrlMap).where(UrlMap.code == code)
    return db.execute(stmt).scalar_one_or_none()


def create_mapping(db: Session, code: str, original_url: str) -> UrlMap:
    m = UrlMap(code=code, original_url=original_url)
    db.add(m)
    db.flush()
    return m


def increment_clicks(db: Session, code: str) -> None:
    stmt = update(UrlMap).where(UrlMap.code == code).values(clicks=UrlMap.clicks + 1)
    db.execute(stmt)
