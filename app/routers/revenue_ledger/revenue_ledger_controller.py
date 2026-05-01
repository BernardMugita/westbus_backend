from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.revenue_ledger.ledger_model import RevenueLedger
from app.routers.revenue_ledger.revenue_ledger_schemas import RevenueLedgerCreate, RevenueLedgerUpdate, RevenueLedgerResponse
from app.config.core.middlewares import requires_auth, requires_admin


class RevenueLedgerController:
    def __init__(self):
        pass

    @requires_admin
    async def create_revenue_ledger(self, db: AsyncSession, data: RevenueLedgerCreate, authorization: str = Header(...), **kwargs) -> RevenueLedgerResponse:
        """
        Create a new RevenueLedger record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (RevenueLedgerCreate): RevenueLedger data
            authorization (str): Bearer token
        Returns:
            RevenueLedgerResponse
        """
        try:
            record = RevenueLedger(
                trip_id=data.trip_id,
                revenue_source=data.revenue_source,
                amount=data.amount,
                revenue_type=data.revenue_type,
                recorded_at=data.recorded_at,
                recorded_by=data.recorded_by,
                notes=data.notes
            )
            
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return RevenueLedgerResponse(status="success", message="RevenueLedger created successfully", payload=record.to_dict())
        except HTTPException as e:
            return RevenueLedgerResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RevenueLedgerResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_revenue_ledger(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> RevenueLedgerResponse:
        """
        Get all RevenueLedger records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            RevenueLedgerResponse
        """
        try:
            result = await db.execute(select(RevenueLedger))
            records = result.scalars().all()
            return RevenueLedgerResponse(
                status="success",
                message="RevenueLedgers retrieved successfully",
                payload=[r.to_dict() for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RevenueLedgerResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_revenue_ledger(self, db: AsyncSession, revenue_id: str, authorization: str = Header(...), **kwargs) -> RevenueLedgerResponse:
        """
        Get a single RevenueLedger by ID.
        Args:
            db (AsyncSession): Database session
            revenue_id (str): RevenueLedger primary key
            authorization (str): Bearer token
        Returns:
            RevenueLedgerResponse
        """
        try:
            result = await db.execute(select(RevenueLedger).where(RevenueLedger.revenue_id == revenue_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RevenueLedger not found")
            return RevenueLedgerResponse(status="success", message="RevenueLedger retrieved successfully", payload=record.to_dict())
        except HTTPException as e:
            return RevenueLedgerResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RevenueLedgerResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_revenue_ledger(self, db: AsyncSession, revenue_id: str, data: RevenueLedgerUpdate, authorization: str = Header(...), **kwargs) -> RevenueLedgerResponse:
        """
        Update a RevenueLedger record. Admin only.
        Args:
            db (AsyncSession): Database session
            revenue_id (str): RevenueLedger primary key
            data (RevenueLedgerUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            RevenueLedgerResponse
        """
        try:
            result = await db.execute(select(RevenueLedger).where(RevenueLedger.revenue_id == revenue_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RevenueLedger not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return RevenueLedgerResponse(status="success", message="RevenueLedger updated successfully", payload=record.to_dict())
        except HTTPException as e:
            return RevenueLedgerResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RevenueLedgerResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_revenue_ledger(self, db: AsyncSession, revenue_id: str, authorization: str = Header(...), **kwargs) -> RevenueLedgerResponse:
        """
        Delete a RevenueLedger record. Admin only.
        Args:
            db (AsyncSession): Database session
            revenue_id (str): RevenueLedger primary key
            authorization (str): Bearer token
        Returns:
            RevenueLedgerResponse
        """
        try:
            result = await db.execute(select(RevenueLedger).where(RevenueLedger.revenue_id == revenue_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RevenueLedger not found")
            await db.delete(record)
            await db.commit()
            return RevenueLedgerResponse(status="success", message="RevenueLedger deleted successfully")
        except HTTPException as e:
            return RevenueLedgerResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RevenueLedgerResponse(status="error", message=str(e)).model_dump()
            )
