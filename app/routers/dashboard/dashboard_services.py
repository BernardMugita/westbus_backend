from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.dashboard.dashboard_schemas import DashboardResponse
from app.routers.dashboard.dashboard_controller import DashboardController

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
controller = DashboardController()

@router.post("/get_data", response_model=DashboardResponse)
async def get_dashboard_data(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_dashboard_data(db=db, authorization=authorization)
