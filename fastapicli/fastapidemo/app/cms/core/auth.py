"""
    author comger@gmail.com
"""
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN
from cms.core import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=config.LOGIN_API)


def verify_password(plain_password: str, hashed_password: str):
    # return hashlib.md5(password).hexdigest() == hashed_password
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str):
    # print(hashlib.md5(password.encode('utf-8')).hexdigest())
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """ 创建Token, 内容为data """
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Security(reusable_oauth2)):
    """ 解码Token 获取明文信息"""
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="验证Token失败"
        )


def get_current_active_user(current_user: Security(get_current_user)):
    if "is_active" in current_user and not current_user['is_active']:
        raise HTTPException(status_code=403, detail="用户已被禁用")
    return current_user


def get_current_active_superuser(current_user: Security(get_current_active_user)):
    if "is_superuser" in current_user and not current_user["is_superuser"]:
        raise HTTPException(
            status_code=403, detail="用户不是超管"
        )
    return current_user
