from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.loans.loans_model import Loan
from app.routers.loans.loans_schemas import LoanCreate, LoanUpdate, LoanResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class LoanController:
    def __init__(self):
        pass

    @requires_admin
    async def create_loans(self, db: AsyncSession, data: LoanCreate, authorization: str = Header(...), **kwargs) -> LoanResponse:
        """
        Create a new Loan record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (LoanCreate): Loan data
            authorization (str): Bearer token
        Returns:
            LoanResponse
        """
        try:
            record = Loan(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return LoanResponse(status="success", message="Loan created successfully", payload=record.__dict__)
        except HTTPException as e:
            return LoanResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_loans(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> LoanResponse:
        """
        Get all Loan records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            LoanResponse
        """
        try:
            result = await db.execute(select(Loan))
            records = result.scalars().all()
            return LoanResponse(
                status="success",
                message="Loans retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_loans(self, db: AsyncSession, loan_id: str, authorization: str = Header(...), **kwargs) -> LoanResponse:
        """
        Get a single Loan by ID.
        Args:
            db (AsyncSession): Database session
            loan_id (str): Loan primary key
            authorization (str): Bearer token
        Returns:
            LoanResponse
        """
        try:
            result = await db.execute(select(Loan).where(Loan.loan_id == loan_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
            return LoanResponse(status="success", message="Loan retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return LoanResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_loans(self, db: AsyncSession, loan_id: str, data: LoanUpdate, authorization: str = Header(...), **kwargs) -> LoanResponse:
        """
        Update a Loan record. Admin only.
        Args:
            db (AsyncSession): Database session
            loan_id (str): Loan primary key
            data (LoanUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            LoanResponse
        """
        try:
            result = await db.execute(select(Loan).where(Loan.loan_id == loan_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return LoanResponse(status="success", message="Loan updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return LoanResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_loans(self, db: AsyncSession, loan_id: str, authorization: str = Header(...), **kwargs) -> LoanResponse:
        """
        Delete a Loan record. Admin only.
        Args:
            db (AsyncSession): Database session
            loan_id (str): Loan primary key
            authorization (str): Bearer token
        Returns:
            LoanResponse
        """
        try:
            result = await db.execute(select(Loan).where(Loan.loan_id == loan_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
            await db.delete(record)
            await db.commit()
            return LoanResponse(status="success", message="Loan deleted successfully")
        except HTTPException as e:
            return LoanResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanResponse(status="error", message=str(e)).model_dump()
            )
