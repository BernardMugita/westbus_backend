from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.trips.trips_schemas import TripCreate, TripUpdate, TripResponse
from app.routers.trips.trips_controller import TripController

router = APIRouter(prefix="/trips", tags=["trips"])
controller = TripController()


@router.post("/", response_model=TripResponse)
async def create_trips(data: TripCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_trips(db=db, data=data, authorization=authorization)


@router.get("/", response_model=TripResponse)
async def get_all_trips(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_trips(db=db, authorization=authorization)


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trips(trip_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_trips(db=db, trip_id=trip_id, authorization=authorization)


@router.patch("/{trip_id}", response_model=TripResponse)
async def update_trips(trip_id: str, data: TripUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_trips(db=db, trip_id=trip_id, data=data, authorization=authorization)


@router.delete("/{trip_id}", response_model=TripResponse)
async def delete_trips(trip_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_trips(db=db, trip_id=trip_id, authorization=authorization)
