from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.payments.payments_schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from app.routers.payments.payments_controller import PaymentController

router = APIRouter(prefix="/payments", tags=["payments"])
controller = PaymentController()


@router.post("/", response_model=PaymentResponse)
async def create_payments(data: PaymentCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_payments(db=db, data=data, authorization=authorization)


@router.get("/", response_model=PaymentResponse)
async def get_all_payments(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_payments(db=db, authorization=authorization)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payments(payment_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_payments(db=db, payment_id=payment_id, authorization=authorization)


@router.patch("/{payment_id}", response_model=PaymentResponse)
async def update_payments(payment_id: str, data: PaymentUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_payments(db=db, payment_id=payment_id, data=data, authorization=authorization)


@router.delete("/{payment_id}", response_model=PaymentResponse)
async def delete_payments(payment_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_payments(db=db, payment_id=payment_id, authorization=authorization)
