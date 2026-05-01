from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.expense.expenses_model import Expense
from app.routers.expense.expense_schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.config.core.middlewares import requires_auth, requires_admin


class ExpenseController:
    def __init__(self):
        pass

    @requires_admin
    async def create_expense(self, db: AsyncSession, data: ExpenseCreate, authorization: str = Header(...), **kwargs) -> ExpenseResponse:
        """
        Create a new Expense record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (ExpenseCreate): Expense data
            authorization (str): Bearer token
        Returns:
            ExpenseResponse
        """
        try:
            record = Expense(
                trip_id=data.trip_id,
                type=data.type,
                amount=data.amount,
                receipt_image=data.receipt_image,
                incident_type=data.incident_type,
            )
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return ExpenseResponse(status="success", message="Expense created successfully", payload=record.to_dict())
        except HTTPException as e:
            return ExpenseResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ExpenseResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_expense(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> ExpenseResponse:
        """
        Get all Expense records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            ExpenseResponse
        """
        try:
            result = await db.execute(select(Expense))
            records = result.scalars().all()
            return ExpenseResponse(
                status="success",
                message="Expenses retrieved successfully",
                payload=[r.to_dict() for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ExpenseResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_expense(self, db: AsyncSession, expense_id: str, authorization: str = Header(...), **kwargs) -> ExpenseResponse:
        """
        Get a single Expense by ID.
        Args:
            db (AsyncSession): Database session
            expense_id (str): Expense primary key
            authorization (str): Bearer token
        Returns:
            ExpenseResponse
        """
        try:
            result = await db.execute(select(Expense).where(Expense.expense_id == expense_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
            return ExpenseResponse(status="success", message="Expense retrieved successfully", payload=record.to_dict())
        except HTTPException as e:
            return ExpenseResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ExpenseResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_expense(self, db: AsyncSession, expense_id: str, data: ExpenseUpdate, authorization: str = Header(...), **kwargs) -> ExpenseResponse:
        """
        Update a Expense record. Admin only.
        Args:
            db (AsyncSession): Database session
            expense_id (str): Expense primary key
            data (ExpenseUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            ExpenseResponse
        """
        try:
            result = await db.execute(select(Expense).where(Expense.expense_id == expense_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return ExpenseResponse(status="success", message="Expense updated successfully", payload=record.to_dict())
        except HTTPException as e:
            return ExpenseResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ExpenseResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_expense(self, db: AsyncSession, expense_id: str, authorization: str = Header(...), **kwargs) -> ExpenseResponse:
        """
        Delete a Expense record. Admin only.
        Args:
            db (AsyncSession): Database session
            expense_id (str): Expense primary key
            authorization (str): Bearer token
        Returns:
            ExpenseResponse
        """
        try:
            result = await db.execute(select(Expense).where(Expense.expense_id == expense_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
            await db.delete(record)
            await db.commit()
            return ExpenseResponse(status="success", message="Expense deleted successfully")
        except HTTPException as e:
            return ExpenseResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ExpenseResponse(status="error", message=str(e)).model_dump()
            )
