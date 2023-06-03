from datetime import timedelta
import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

import bcrypt
import config
from db import models, schemas
from db.db import get_session, session_commit
from .models import Token, Session
from .utils import userAuthenticate, createAccessToken

clientsRouter = APIRouter()
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="api/v1/clients/token")

@clientsRouter.post("/create", response_model=schemas.Clients, status_code=status.HTTP_201_CREATED)
async def createClient(client: schemas.ClientsCreate, session: AsyncSession = Depends(get_session)):
    """
    Registration request.
    Args:
        client: form with client credentials.
        session: current db session instance.
    Returns:
        Clients: model with client parameteres.
    """
    hashed_password = bcrypt.hashpw(client.password.encode(), bcrypt.gensalt())
    clientData = {
        "fio": client.fio,
        "phone": client.phone,
        "email": client.email,
        "password": hashed_password.decode(),
        "telegram": client.telegram
    }

    queryClientCreate = models.clients.insert().values(**clientData)
    result: AsyncResult = await session.execute(queryClientCreate)
    await session_commit(
        IntegrityError, HTTPException(
            status_code=400,
            detail="User with this phone or email already exists."
        ), session
    )
    lastRecordId: int = result.inserted_primary_key[0]
    response = schemas.Clients(**clientData, id=lastRecordId)
    return response

@clientsRouter.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def createToken(formData: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    """
    Create access token request.
    Args:
        formData: form with OAuth2 parameteres. Most important are email and password.
    Returns:
        token: dictionary with access token and its type.
    """
    client = await userAuthenticate(formData, Session(session=session))
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await createAccessToken(
        data={"sub": client.email}, expires_delta=access_token_expires
    )
    resp = Token(access_token=access_token, token_type="bearer", user_id=client.id)
    
    return resp
