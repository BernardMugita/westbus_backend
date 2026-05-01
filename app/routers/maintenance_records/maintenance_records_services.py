from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.maintenance_records.maintenance_records_schemas import MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordResponse
from app.routers.maintenance_records.maintenance_records_controller import MaintenanceRecordController

router = APIRouter(prefix="/maintenance-records", tags=["maintenance-records"])
controller = MaintenanceRecordController()


@router.post("/add_maintenance_record", response_model=MaintenanceRecordResponse)
async def create_maintenance_records(data: MaintenanceRecordCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_maintenance_records(db=db, data=data, authorization=authorization)


@router.post("/get_all_maintenance_records", response_model=MaintenanceRecordResponse)
async def get_all_maintenance_records(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_maintenance_records(db=db, authorization=authorization)


@router.post("/get_maintenance_record/{maintenance_id}", response_model=MaintenanceRecordResponse)
async def get_maintenance_records(maintenance_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_maintenance_records(db=db, maintenance_id=maintenance_id, authorization=authorization)


@router.post("/update_maintenance_record/{maintenance_id}", response_model=MaintenanceRecordResponse)
async def update_maintenance_records(maintenance_id: str, data: MaintenanceRecordUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_maintenance_records(db=db, maintenance_id=maintenance_id, data=data, authorization=authorization)


@router.post("/delete_maintenance_record/{maintenance_id}", response_model=MaintenanceRecordResponse)
async def delete_maintenance_records(maintenance_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_maintenance_records(db=db, maintenance_id=maintenance_id, authorization=authorization)
