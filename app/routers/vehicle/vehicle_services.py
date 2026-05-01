from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.vehicle.vehicle_schemas import VehicleCreate, VehicleUpdate, VehicleResponse
from app.routers.vehicle.vehicle_controller import VehicleController

router = APIRouter(prefix="/vehicles", tags=["vehicles"])
controller = VehicleController()


@router.post("/create_vehicle", response_model=VehicleResponse)
async def create_vehicle(vehicle_create: VehicleCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_vehicle(db=db, vehicle_create=vehicle_create, authorization=authorization)

@router.post("/get_all_vehicles", response_model=VehicleResponse)
async def get_all_vehicle(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_vehicles(db=db, authorization=authorization)


@router.post("/get_vehicle/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_vehicle(db=db, vehicle_id=vehicle_id, authorization=authorization)


@router.post("/update_vehicle/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(vehicle_id: str, vehicle_update: VehicleUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_vehicle(db=db, vehicle_id=vehicle_id, vehicle_update=vehicle_update, authorization=authorization)


@router.post("/delete_vehicle/{vehicle_id}", response_model=VehicleResponse)
async def delete_vehicle(vehicle_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_vehicle(db=db, vehicle_id=vehicle_id, authorization=authorization)
