from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.insurance_policy.policy_model import InsurancePolicy
from app.routers.insurance_policy.insurance_policy_schemas import InsurancePolicyCreate, InsurancePolicyUpdate, InsurancePolicyResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class InsurancePolicyController:
    def __init__(self):
        pass

    @requires_admin
    async def create_insurance_policy(self, db: AsyncSession, data: InsurancePolicyCreate, authorization: str = Header(...), **kwargs) -> InsurancePolicyResponse:
        """
        Create a new InsurancePolicy record. Admin only.
        Args:
            db (AsyncSession): Database session
            data (InsurancePolicyCreate): InsurancePolicy data
            authorization (str): Bearer token
        Returns:
            InsurancePolicyResponse
        """
        try:
            record = InsurancePolicy(**data.model_dump())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return InsurancePolicyResponse(status="success", message="InsurancePolicy created successfully", payload=record.__dict__)
        except HTTPException as e:
            return InsurancePolicyResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsurancePolicyResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_all_insurance_policy(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> InsurancePolicyResponse:
        """
        Get all InsurancePolicy records.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            InsurancePolicyResponse
        """
        try:
            result = await db.execute(select(InsurancePolicy))
            records = result.scalars().all()
            return InsurancePolicyResponse(
                status="success",
                message="InsurancePolicys retrieved successfully",
                payload=[r.__dict__ for r in records]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsurancePolicyResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def get_insurance_policy(self, db: AsyncSession, insurance_id: str, authorization: str = Header(...), **kwargs) -> InsurancePolicyResponse:
        """
        Get a single InsurancePolicy by ID.
        Args:
            db (AsyncSession): Database session
            insurance_id (str): InsurancePolicy primary key
            authorization (str): Bearer token
        Returns:
            InsurancePolicyResponse
        """
        try:
            result = await db.execute(select(InsurancePolicy).where(InsurancePolicy.insurance_id == insurance_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InsurancePolicy not found")
            return InsurancePolicyResponse(status="success", message="InsurancePolicy retrieved successfully", payload=record.__dict__)
        except HTTPException as e:
            return InsurancePolicyResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsurancePolicyResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_insurance_policy(self, db: AsyncSession, insurance_id: str, data: InsurancePolicyUpdate, authorization: str = Header(...), **kwargs) -> InsurancePolicyResponse:
        """
        Update a InsurancePolicy record. Admin only.
        Args:
            db (AsyncSession): Database session
            insurance_id (str): InsurancePolicy primary key
            data (InsurancePolicyUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            InsurancePolicyResponse
        """
        try:
            result = await db.execute(select(InsurancePolicy).where(InsurancePolicy.insurance_id == insurance_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InsurancePolicy not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(record, field, value)
            await db.commit()
            await db.refresh(record)
            return InsurancePolicyResponse(status="success", message="InsurancePolicy updated successfully", payload=record.__dict__)
        except HTTPException as e:
            return InsurancePolicyResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsurancePolicyResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_insurance_policy(self, db: AsyncSession, insurance_id: str, authorization: str = Header(...), **kwargs) -> InsurancePolicyResponse:
        """
        Delete a InsurancePolicy record. Admin only.
        Args:
            db (AsyncSession): Database session
            insurance_id (str): InsurancePolicy primary key
            authorization (str): Bearer token
        Returns:
            InsurancePolicyResponse
        """
        try:
            result = await db.execute(select(InsurancePolicy).where(InsurancePolicy.insurance_id == insurance_id))
            record = result.scalar_one_or_none()
            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="InsurancePolicy not found")
            await db.delete(record)
            await db.commit()
            return InsurancePolicyResponse(status="success", message="InsurancePolicy deleted successfully")
        except HTTPException as e:
            return InsurancePolicyResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=InsurancePolicyResponse(status="error", message=str(e)).model_dump()
            )
