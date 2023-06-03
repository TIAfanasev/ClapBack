from fastapi import APIRouter

from buildings.services import buildingsRouter
from clients.services import clientsRouter

apiRouter = APIRouter(prefix="/api/v1")
apiRouter.include_router(clientsRouter, prefix="/clients")
apiRouter.include_router(buildingsRouter, prefix="/buildings")
