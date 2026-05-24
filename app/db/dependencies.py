from collections.abc import Generator

from sqlalchemy.orm import Session

from app.db.connection import SessionLocal

def getDB() -> Generator[Session, None, None]: 
    db = SessionLocal()

    try:
      yield db
    finally:
       db.close()
        