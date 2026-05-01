from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.driver.driver_schemas import DriverCreate, DriverUpdate, DriverResponse
from app.routers.driver.driver_controller import DriverController

router = APIRouter(prefix="/drivers", tags=["drivers"])
controller = DriverController()


@router.post("/add_driver", response_model=DriverResponse)
async def create_driver(data: DriverCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_driver(db=db, data=data, authorization=authorization)


@router.post("/get_all_drivers", response_model=DriverResponse)
async def get_all_driver(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_driver(db=db, authorization=authorization)


@router.post("/get_driver/{driver_id}", response_model=DriverResponse)
async def get_driver(driver_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_driver(db=db, driver_id=driver_id, authorization=authorization)


@router.post("/update_driver/{driver_id}", response_model=DriverResponse)
async def update_driver(driver_id: str, data: DriverUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_driver(db=db, driver_id=driver_id, data=data, authorization=authorization)


@router.post("/delete_driver/{driver_id}", response_model=DriverResponse)
async def delete_driver(driver_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_driver(db=db, driver_id=driver_id, authorization=authorization)
