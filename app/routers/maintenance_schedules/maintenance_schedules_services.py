from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.maintenance_schedules.maintenance_schedules_schemas import MaintenanceScheduleCreate, MaintenanceScheduleUpdate, MaintenanceScheduleResponse
from app.routers.maintenance_schedules.maintenance_schedules_controller import MaintenanceScheduleController

router = APIRouter(prefix="/maintenance-schedules", tags=["maintenance-schedules"])
controller = MaintenanceScheduleController()


@router.post("/add_maintenance_schedule", response_model=MaintenanceScheduleResponse)
async def create_maintenance_schedules(data: MaintenanceScheduleCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_maintenance_schedules(db=db, data=data, authorization=authorization)


@router.post("/get_all_maintenance_schedules", response_model=MaintenanceScheduleResponse)
async def get_all_maintenance_schedules(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_maintenance_schedules(db=db, authorization=authorization)


@router.post("/get_maintenance_schedule/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def get_maintenance_schedules(schedule_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_maintenance_schedules(db=db, schedule_id=schedule_id, authorization=authorization)


@router.post("/update_maintenance_schedule/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def update_maintenance_schedules(schedule_id: str, data: MaintenanceScheduleUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_maintenance_schedules(db=db, schedule_id=schedule_id, data=data, authorization=authorization)


@router.post("/delete_maintenance_schedule/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def delete_maintenance_schedules(schedule_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_maintenance_schedules(db=db, schedule_id=schedule_id, authorization=authorization)
