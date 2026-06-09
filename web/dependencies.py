"""
FastAPI dependencies (auth, db, queue).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Generator

from src.config import settings
from src.db.models import User
from src.task_queue_db import TaskQueueDB
from src.db.session import get_session as _get_sync_session

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """Sync DB session."""
    db = _get_sync_session()
    try:
        yield db
    finally:
        db.close()


def get_task_queue() -> TaskQueueDB:
    """Return a TaskQueueDB instance."""
    return TaskQueueDB()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """JWT auth dependency."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account disabled")
    return user
