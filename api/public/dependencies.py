# api/public/dependencies.py

from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from api.database import get_session
from api.public.user.models import User
from api.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Esquema de autenticación inválido",
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No se encontraron credenciales de autenticación",
            )

def get_current_user(
    token: str = Depends(JWTBearer()),
    db: Session = Depends(get_session)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar el token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.exec(select(User).where(User.id == int(user_id))).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Nueva clase OptionalJWTBearer
class OptionalJWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(OptionalJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: Optional[HTTPAuthorizationCredentials] = await super(OptionalJWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                # Puedes elegir lanzar una excepción o simplemente retornar None
                return None
            return credentials.credentials
        return None

def get_optional_current_user(
    token: Optional[str] = Depends(OptionalJWTBearer()),
    db: Session = Depends(get_session)
) -> Optional[User]:
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = db.exec(select(User).where(User.id == int(user_id))).first()
        return user
    except JWTError:
        return None
