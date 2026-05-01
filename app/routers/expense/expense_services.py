from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.expense.expense_schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.routers.expense.expense_controller import ExpenseController

router = APIRouter(prefix="/expenses", tags=["expenses"])
controller = ExpenseController()


@router.post("/", response_model=ExpenseResponse)
async def create_expense(data: ExpenseCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_expense(db=db, data=data, authorization=authorization)


@router.get("/", response_model=ExpenseResponse)
async def get_all_expense(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_expense(db=db, authorization=authorization)


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_expense(db=db, expense_id=expense_id, authorization=authorization)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: str, data: ExpenseUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_expense(db=db, expense_id=expense_id, data=data, authorization=authorization)


@router.delete("/{expense_id}", response_model=ExpenseResponse)
async def delete_expense(expense_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_expense(db=db, expense_id=expense_id, authorization=authorization)
