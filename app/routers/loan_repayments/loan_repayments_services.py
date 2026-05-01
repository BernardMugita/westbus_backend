from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.loan_repayments.loan_repayments_schemas import LoanRepaymentCreate, LoanRepaymentUpdate, LoanRepaymentResponse
from app.routers.loan_repayments.loan_repayments_controller import LoanRepaymentController

router = APIRouter(prefix="/loan-repayments", tags=["loan-repayments"])
controller = LoanRepaymentController()


@router.post("/make_repayment", response_model=LoanRepaymentResponse)
async def create_loan_repayments(data: LoanRepaymentCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_loan_repayments(db=db, data=data, authorization=authorization)


@router.post("/get_all_repayments", response_model=LoanRepaymentResponse)
async def get_all_loan_repayments(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_loan_repayments(db=db, authorization=authorization)


@router.post("/get_repayment/{repayment_id}", response_model=LoanRepaymentResponse)
async def get_loan_repayments(repayment_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_loan_repayments(db=db, repayment_id=repayment_id, authorization=authorization)


@router.post("/update_repayment/{repayment_id}", response_model=LoanRepaymentResponse)
async def update_loan_repayments(repayment_id: str, data: LoanRepaymentUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_loan_repayments(db=db, repayment_id=repayment_id, data=data, authorization=authorization)


@router.post("/delete_repayment/{repayment_id}", response_model=LoanRepaymentResponse)
async def delete_loan_repayments(repayment_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_loan_repayments(db=db, repayment_id=repayment_id, authorization=authorization)
