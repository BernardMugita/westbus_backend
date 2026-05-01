from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.revenue_ledger.revenue_ledger_schemas import RevenueLedgerCreate, RevenueLedgerUpdate, RevenueLedgerResponse
from app.routers.revenue_ledger.revenue_ledger_controller import RevenueLedgerController

router = APIRouter(prefix="/revenue-ledger", tags=["revenue-ledger"])
controller = RevenueLedgerController()


@router.post("/", response_model=RevenueLedgerResponse)
async def create_revenue_ledger(data: RevenueLedgerCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_revenue_ledger(db=db, data=data, authorization=authorization)


@router.get("/", response_model=RevenueLedgerResponse)
async def get_all_revenue_ledger(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_revenue_ledger(db=db, authorization=authorization)


@router.get("/{revenue_id}", response_model=RevenueLedgerResponse)
async def get_revenue_ledger(revenue_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_revenue_ledger(db=db, revenue_id=revenue_id, authorization=authorization)


@router.patch("/{revenue_id}", response_model=RevenueLedgerResponse)
async def update_revenue_ledger(revenue_id: str, data: RevenueLedgerUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_revenue_ledger(db=db, revenue_id=revenue_id, data=data, authorization=authorization)


@router.delete("/{revenue_id}", response_model=RevenueLedgerResponse)
async def delete_revenue_ledger(revenue_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_revenue_ledger(db=db, revenue_id=revenue_id, authorization=authorization)
