from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.loans.loans_schemas import LoanCreate, LoanUpdate, LoanResponse
from app.routers.loans.loans_controller import LoanController

router = APIRouter(prefix="/loans", tags=["loans"])
controller = LoanController()


@router.post("/add_loan", response_model=LoanResponse)
async def create_loans(data: LoanCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_loans(db=db, data=data, authorization=authorization)


@router.post("/get_all_loans", response_model=LoanResponse)
async def get_all_loans(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_loans(db=db, authorization=authorization)


@router.post("/get_loan/{loan_id}", response_model=LoanResponse)
async def get_loans(loan_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_loans(db=db, loan_id=loan_id, authorization=authorization)


@router.post("/update_loan/{loan_id}", response_model=LoanResponse)
async def update_loans(loan_id: str, data: LoanUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_loans(db=db, loan_id=loan_id, data=data, authorization=authorization)


@router.post("/delete_loan/{loan_id}", response_model=LoanResponse)
async def delete_loans(loan_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_loans(db=db, loan_id=loan_id, authorization=authorization)
