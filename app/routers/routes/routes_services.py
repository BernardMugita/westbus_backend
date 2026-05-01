from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.routes.routes_schemas import RouteCreate, RouteUpdate, RouteResponse
from app.routers.routes.routes_controller import RouteController

router = APIRouter(prefix="/routes", tags=["routes"])
controller = RouteController()


@router.post("/add_route", response_model=RouteResponse)
async def create_routes(data: RouteCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_routes(db=db, data=data, authorization=authorization)


@router.post("/get_all_routes", response_model=RouteResponse)
async def get_all_routes(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_routes(db=db, authorization=authorization)


@router.post("/get_route/{route_id}", response_model=RouteResponse)
async def get_routes(route_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_routes(db=db, route_id=route_id, authorization=authorization)


@router.post("/update_route/{route_id}", response_model=RouteResponse)
async def update_routes(route_id: str, data: RouteUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_routes(db=db, route_id=route_id, data=data, authorization=authorization)


@router.post("/delete_route/{route_id}", response_model=RouteResponse)
async def delete_routes(route_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_routes(db=db, route_id=route_id, authorization=authorization)
