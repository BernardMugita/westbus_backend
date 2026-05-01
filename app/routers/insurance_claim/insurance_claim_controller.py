from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.insurance_claim.claims_model import InsuranceClaim
from app.routers.insurance_claim.insurance_claim_schemas import InsuranceClaimCreate, InsuranceClaimUpdate, InsuranceClaimResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class InsuranceClaimController:
    def __init__(self):
        pass

    @requires_admin
    async def create_insurance_claim(self, db: AsyncSession, data: InsuranceClaimCreate, authorization: str = Header(...), **kwargs) -> InsuranceClaimResponse:
        """
        Create a new InsuranceClaim record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (InsuranceClaimCreate): InsuranceClaim data
            authorization (str): Bearer token
        Returns:
            InsuranceClaimResponse
        """
        try:
            record = InsuranceClaim(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return InsuranceClaimResponse(status="success", message="InsuranceClaim created successfully", payload=record.__dict__)
        except HTTPException as e:
            return InsuranceClaimResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsuranceClaimResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_insurance_claim(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> InsuranceClaimResponse:
        """
        Get all InsuranceClaim records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            InsuranceClaimResponse
        """
        try:
            result = await db.execute(select(InsuranceClaim))
            records = result.scalars().all()
            return InsuranceClaimResponse(
                status="success",
                message="InsuranceClaims retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsuranceClaimResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_insurance_claim(self, db: AsyncSession, claim_id: str, authorization: str = Header(...), **kwargs) -> InsuranceClaimResponse:
        """
        Get a single InsuranceClaim by ID.
        Args:
            db (AsyncSession): Database session
            claim_id (str): InsuranceClaim primary key
            authorization (str): Bearer token
        Returns:
            InsuranceClaimResponse
        """
        try:
            result = await db.execute(select(InsuranceClaim).where(InsuranceClaim.claim_id == claim_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InsuranceClaim not found")
            return InsuranceClaimResponse(status="success", message="InsuranceClaim retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return InsuranceClaimResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsuranceClaimResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_insurance_claim(self, db: AsyncSession, claim_id: str, data: InsuranceClaimUpdate, authorization: str = Header(...), **kwargs) -> InsuranceClaimResponse:
        """
        Update a InsuranceClaim record. Admin only.
        Args:
            db (AsyncSession): Database session
            claim_id (str): InsuranceClaim primary key
            data (InsuranceClaimUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            InsuranceClaimResponse
        """
        try:
            result = await db.execute(select(InsuranceClaim).where(InsuranceClaim.claim_id == claim_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InsuranceClaim not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return InsuranceClaimResponse(status="success", message="InsuranceClaim updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return InsuranceClaimResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsuranceClaimResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_insurance_claim(self, db: AsyncSession, claim_id: str, authorization: str = Header(...), **kwargs) -> InsuranceClaimResponse:
        """
        Delete a InsuranceClaim record. Admin only.
        Args:
            db (AsyncSession): Database session
            claim_id (str): InsuranceClaim primary key
            authorization (str): Bearer token
        Returns:
            InsuranceClaimResponse
        """
        try:
            result = await db.execute(select(InsuranceClaim).where(InsuranceClaim.claim_id == claim_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InsuranceClaim not found")
            await db.delete(record)
            await db.commit()
            return InsuranceClaimResponse(status="success", message="InsuranceClaim deleted successfully")
        except HTTPException as e:
            return InsuranceClaimResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsuranceClaimResponse(status="error", message=str(e)).model_dump()
            )
