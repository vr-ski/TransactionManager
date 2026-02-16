from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return int(user_id)
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e


# Passlib context for hashing + verifying
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Compare a plain-text password with a hashed password.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, password_hash)


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    Returns the hashed password.
    """
    return pwd_context.hash(password)
