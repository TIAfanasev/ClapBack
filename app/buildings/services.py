import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult

from clients.models import Session
from clients.services import oauth2Scheme
from clients.utils import getCurrentClient
from db import models, schemas
from db.db import get_session, session_commit

buildingsRouter = APIRouter()

@buildingsRouter.get("/get-all", response_model=list[schemas.Buildings], status_code=status.HTTP_200_OK)
async def getBuildings(
        token: str = Depends(oauth2Scheme),
        session: AsyncSession = Depends(get_session)
    ):
    """
    Request to get all buildings.
    Args:
        _: token for checking whether user is authorized.
        session: db session instance.
    Returns:
        List of Building items.
    """

    queryGetBuildings = models.buildings.select()
    result: AsyncResult = await session.execute(queryGetBuildings)
    buildings = result.all()
    if buildings:
        response = [schemas.Buildings(**item._asdict()) for item in buildings]
    else:
        response = []
    return response

@buildingsRouter.post("/{building_id}/create")
async def createApp(
    building_id: int,
    token: str = Depends(oauth2Scheme),
    session: AsyncSession = Depends(get_session)
):
    """
    Request to create an application for a building.
    Args:
        app: application form.
        token: token for checking whether user is authorized.
        session: db session instance.
    Returns:
        Application item.
    """
    clientRow = await getCurrentClient(Session(session=session), token)
    client = schemas.Clients(**clientRow._asdict())

    buildingQuery = models.buildings.select().where(models.buildings.c.id == building_id)
    result: AsyncResult = await session.execute(buildingQuery)
    building = result.one_or_none()

    if client.id not in building._asdict()["buildings_used"]:
        newList = building._asdict()["buildings_used"]
        newList.append(client.id)
        updateCardQuery = models.buildings.update().where(
            models.buildings.c.id==building_id
        ).values(buildings_used=newList)
        await session.execute(updateCardQuery)

        appData = {
            "client": client.id,
            "building": building_id,
            "date": dt.datetime.now(),
            "ready": False,
            "used": True
        }
        queryAppCreate = models.apps.insert().values(**appData)
        result: AsyncResult = await session.execute(queryAppCreate)
        await session_commit(
            IntegrityError, HTTPException(
                status_code=400,
                detail="User with this phone or email already exists."
            ), session
        )
        lastRecordId: int = result.inserted_primary_key[0]
        response = schemas.Apps(**appData, id=lastRecordId)
        return response
    else:
        newList = building._asdict()["buildings_used"]
        newList.remove(client.id)
        updateCardQuery = models.buildings.update().where(models.buildings.c.id==building_id).values(buildings_used=newList)
        await session.execute(updateCardQuery)

        queryAppDelete = models.apps.delete().where(
            and_(
                models.apps.c.client == client.id,
                models.apps.c.building == building_id
            )
        )
        await session.execute(queryAppDelete)
        await session_commit(
            IntegrityError, HTTPException(
                status_code=500,
                detail="Something went wrong."
            ), session
        )
