from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.payments.payments_model import Payment
from app.routers.payments.payments_schemas import PaymentCreate, PaymentUpdate, PaymentResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class PaymentController:
    def __init__(self):
        pass

    @requires_admin
    async def create_payments(self, db: AsyncSession, data: PaymentCreate, authorization: str = Header(...), **kwargs) -> PaymentResponse:
        """
        Create a new Payment record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (PaymentCreate): Payment data
            authorization (str): Bearer token
        Returns:
            PaymentResponse
        """
        try:
            record = Payment(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return PaymentResponse(status="success", message="Payment created successfully", payload=record.__dict__)
        except HTTPException as e:
            return PaymentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=PaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_payments(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> PaymentResponse:
        """
        Get all Payment records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            PaymentResponse
        """
        try:
            result = await db.execute(select(Payment))
            records = result.scalars().all()
            return PaymentResponse(
                status="success",
                message="Payments retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=PaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_payments(self, db: AsyncSession, payment_id: str, authorization: str = Header(...), **kwargs) -> PaymentResponse:
        """
        Get a single Payment by ID.
        Args:
            db (AsyncSession): Database session
            payment_id (str): Payment primary key
            authorization (str): Bearer token
        Returns:
            PaymentResponse
        """
        try:
            result = await db.execute(select(Payment).where(Payment.payment_id == payment_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
            return PaymentResponse(status="success", message="Payment retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return PaymentResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=PaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_payments(self, db: AsyncSession, payment_id: str, data: PaymentUpdate, authorization: str = Header(...), **kwargs) -> PaymentResponse:
        """
        Update a Payment record. Admin only.
        Args:
            db (AsyncSession): Database session
            payment_id (str): Payment primary key
            data (PaymentUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            PaymentResponse
        """
        try:
            result = await db.execute(select(Payment).where(Payment.payment_id == payment_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return PaymentResponse(status="success", message="Payment updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return PaymentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=PaymentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_payments(self, db: AsyncSession, payment_id: str, authorization: str = Header(...), **kwargs) -> PaymentResponse:
        """
        Delete a Payment record. Admin only.
        Args:
            db (AsyncSession): Database session
            payment_id (str): Payment primary key
            authorization (str): Bearer token
        Returns:
            PaymentResponse
        """
        try:
            result = await db.execute(select(Payment).where(Payment.payment_id == payment_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
            await db.delete(record)
            await db.commit()
            return PaymentResponse(status="success", message="Payment deleted successfully")
        except HTTPException as e:
            return PaymentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=PaymentResponse(status="error", message=str(e)).model_dump()
            )
