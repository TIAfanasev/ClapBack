import os
from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncResult

import config
from db import models, schemas
from .models import Session

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def userAuthenticate(
        formData: OAuth2PasswordRequestForm,
        session: Session
    ) -> schemas.Clients:
    """
    Function to check whether user exists and its password is true.
    Args:
        form_data: username and password from OAuth2 form.
    Returns:
        Pydantic model of User
    """
    queryUserModel = models.clients.select().where(models.clients.c.email == formData.username)
    result: AsyncResult = await session.session.execute(queryUserModel)
    clientsModel = result.one()
    if not clientsModel:
        raise HTTPException(status_code=400, detail=f"No user with {formData.username} found")
    
    client = schemas.Clients(**clientsModel._asdict())
    # password checking
    if not bcrypt.checkpw(formData.password.encode('utf-8'), client.password.encode()):
        raise HTTPException(
            status_code=400,
            detail=f"No user with {formData.username} found"
        )

    
    return client

async def createAccessToken(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Function to create access token.
    Args:
        data: dictionary with token data.
        expires_delta: time before token expires.
    Returns:
        Encoded JWT token.
    """
    to_encode = data.copy() # copy of dictionary we need to encode
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY)
    return encoded_jwt

async def getCurrentClient(session: Session, token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/v1/users/token"))):
    """
    Function to get current user by its access token.
    Args:
        token: access token of current user.
        session: Pydantic model of AsyncSession object.
    Returns:
        Instance of SQLAlchemy Record class with user info.
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY)
        email: EmailStr = payload.get("sub") # getting email from token
        if not email:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    queryClient = models.clients.select().where(models.clients.c.email == email)
    result: AsyncResult = await session.session.execute(queryClient) # getting user from db
    client = result.one_or_none()
    if not client:
        raise credentials_exception
    
    return client
