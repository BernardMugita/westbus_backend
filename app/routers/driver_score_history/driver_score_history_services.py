from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.driver_score_history.driver_score_history_schemas import DriverScoreHistoryCreate, DriverScoreHistoryUpdate, DriverScoreHistoryResponse
from app.routers.driver_score_history.driver_score_history_controller import DriverScoreHistoryController

router = APIRouter(prefix="/driver-score-history", tags=["driver-score-history"])
controller = DriverScoreHistoryController()


@router.post("/", response_model=DriverScoreHistoryResponse)
async def create_driver_score_history(data: DriverScoreHistoryCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_driver_score_history(db=db, data=data, authorization=authorization)


@router.get("/", response_model=DriverScoreHistoryResponse)
async def get_all_driver_score_history(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_driver_score_history(db=db, authorization=authorization)


@router.get("/{score_id}", response_model=DriverScoreHistoryResponse)
async def get_driver_score_history(score_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_driver_score_history(db=db, score_id=score_id, authorization=authorization)


@router.patch("/{score_id}", response_model=DriverScoreHistoryResponse)
async def update_driver_score_history(score_id: str, data: DriverScoreHistoryUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_driver_score_history(db=db, score_id=score_id, data=data, authorization=authorization)


@router.delete("/{score_id}", response_model=DriverScoreHistoryResponse)
async def delete_driver_score_history(score_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_driver_score_history(db=db, score_id=score_id, authorization=authorization)
