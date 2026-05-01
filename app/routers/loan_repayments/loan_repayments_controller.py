from decimal import Decimal

from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.loan_repayments.loan_repayments_model import LoanRepayment
from app.routers.loans.loans_model import Loan
from app.routers.loan_repayments.loan_repayments_schemas import LoanRepaymentCreate, LoanRepaymentUpdate, LoanRepaymentResponse
from app.config.core.middlewares import requires_auth, requires_admin


class LoanRepaymentController:
    def __init__(self):
        pass

    @requires_admin
    async def create_loan_repayments(self, db: AsyncSession, data: LoanRepaymentCreate, authorization: str = Header(...), **kwargs) -> LoanRepaymentResponse:
        try:
            loan_result = await db.execute(select(Loan).where(Loan.loan_id == data.loan_id))
            loan = loan_result.scalar_one_or_none()

            if not loan:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated Loan not found")
            
            outstanding_balance = float(loan.total_payable) - float(data.amount_paid)
            loan.total_payable -= Decimal(str(data.amount_paid))

            record = LoanRepayment(
                loan_id=data.loan_id,
                payment_date=data.payment_date,
                amount_paid=data.amount_paid,
                principal_portion=data.principal_portion,
                interest_portion=data.interest_portion,
                outstanding_balance=outstanding_balance,
                receipt_ref=data.receipt_ref
            )

            db.add(record)
            await db.commit()
            await db.refresh(loan)
            await db.refresh(record)

            return LoanRepaymentResponse(status="success", message="LoanRepayment created successfully", payload=record.to_dict())

        except HTTPException as e:
            return LoanRepaymentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanRepaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_loan_repayments(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> LoanRepaymentResponse:
        """
        Get all LoanRepayment records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            LoanRepaymentResponse
        """
        try:
            result = await db.execute(select(LoanRepayment))
            records = result.scalars().all()
            return LoanRepaymentResponse(
                status="success",
                message="LoanRepayments retrieved successfully",
                payload=[r.to_dict() for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanRepaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_loan_repayments(self, db: AsyncSession, repayment_id: str, authorization: str = Header(...), **kwargs) -> LoanRepaymentResponse:
        """
        Get a single LoanRepayment by ID.
        Args:
            db (AsyncSession): Database session
            repayment_id (str): LoanRepayment primary key
            authorization (str): Bearer token
        Returns:
            LoanRepaymentResponse
        """
        try:
            result = await db.execute(select(LoanRepayment).where(LoanRepayment.repayment_id == repayment_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoanRepayment not found")
            return LoanRepaymentResponse(status="success", message="LoanRepayment retrieved successfully", payload=record.to_dict())
        except HTTPException as e:
            return LoanRepaymentResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanRepaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_loan_repayments(self, db: AsyncSession, repayment_id: str, data: LoanRepaymentUpdate, authorization: str = Header(...), **kwargs) -> LoanRepaymentResponse:
        """
        Update a LoanRepayment record. Admin only.
        Args:
            db (AsyncSession): Database session
            repayment_id (str): LoanRepayment primary key
            data (LoanRepaymentUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            LoanRepaymentResponse
        """
        try:
            result = await db.execute(select(LoanRepayment).where(LoanRepayment.repayment_id == repayment_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoanRepayment not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return LoanRepaymentResponse(status="success", message="LoanRepayment updated successfully", payload=record.to_dict())
        except HTTPException as e:
            return LoanRepaymentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanRepaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_loan_repayments(self, db: AsyncSession, repayment_id: str, authorization: str = Header(...), **kwargs) -> LoanRepaymentResponse:
        """
        Delete a LoanRepayment record. Admin only.
        Args:
            db (AsyncSession): Database session
            repayment_id (str): LoanRepayment primary key
            authorization (str): Bearer token
        Returns:
            LoanRepaymentResponse
        """
        try:
            result = await db.execute(select(LoanRepayment).where(LoanRepayment.repayment_id == repayment_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LoanRepayment not found")
            await db.delete(record)
            await db.commit()
            return LoanRepaymentResponse(status="success", message="LoanRepayment deleted successfully")
        except HTTPException as e:
            return LoanRepaymentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=LoanRepaymentResponse(status="error", message=str(e)).model_dump()
            )
