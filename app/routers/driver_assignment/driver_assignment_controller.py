from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.driver_assignment.assignment_model import DriverAssignment
from app.routers.driver_assignment.driver_assignment_schemas import DriverAssignmentCreate, DriverAssignmentUpdate, DriverAssignmentResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class DriverAssignmentController:
    def __init__(self):
        pass 

    @requires_admin
    async def create_driver_assignment(self, db: AsyncSession, data: DriverAssignmentCreate, authorization: str = Header(...), **kwargs) -> DriverAssignmentResponse:
        """
        Create a new DriverAssignment assignment. Admin only.
        Args:
            db (AsyncSession): Database session
            data (DriverAssignmentCreate): DriverAssignment data
            authorization (str): Bearer token
        Returns:
            DriverAssignmentResponse
        """
        try:
            assignment = DriverAssignment(
                driver_id=data.driver_id,
                vehicle_id=data.vehicle_id,
                start_date=data.start_date,
                end_date=data.end_date,
                is_current=data.is_current
            )
            
            db.add(assignment)
            await db.commit()
            await db.refresh(assignment)
            return DriverAssignmentResponse(status="success", message="Driver Assigned Succesfully", payload=assignment.to_dict())
        except HTTPException as e:
            return DriverAssignmentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverAssignmentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_driver_assignment(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> DriverAssignmentResponse:
        """
        Get all DriverAssignment assignments.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            DriverAssignmentResponse
        """
        try:
            driver_assignment = await db.execute(select(DriverAssignment))
            assignments = driver_assignment.scalars().all()
            
            return DriverAssignmentResponse(
                status="success",
                message="Driver Assignments loaded successfully",
                payload=[r.to_dict() for r in assignments]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverAssignmentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_driver_assignment(self, db: AsyncSession, assignment_id: str, authorization: str = Header(...), **kwargs) -> DriverAssignmentResponse:
        """
        Get a single DriverAssignment by ID.
        Args:
            db (AsyncSession): Database session
            assignment_id (str): DriverAssignment primary key
            authorization (str): Bearer token
        Returns:
            DriverAssignmentResponse
        """
        try:
            driver_assignment = await db.execute(select(DriverAssignment).where(DriverAssignment.assignment_id == assignment_id))
            assignment = driver_assignment.scalar_one_or_none()
            
            if not assignment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DriverAssignment not found")
            return DriverAssignmentResponse(status="success", message="Driver Assignment loaded successfully", payload=assignment.to_dict())
        except HTTPException as e:
            return DriverAssignmentResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverAssignmentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_driver_assignment(self, db: AsyncSession, assignment_id: str, data: DriverAssignmentUpdate, authorization: str = Header(...), **kwargs) -> DriverAssignmentResponse:
        """
        Update a DriverAssignment assignment. Admin only.
        Args:
            db (AsyncSession): Database session
            assignment_id (str): DriverAssignment primary key
            data (DriverAssignmentUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            DriverAssignmentResponse
        """
        try:
            driver_assignment = await db.execute(select(DriverAssignment).where(DriverAssignment.assignment_id == assignment_id))
            assignment = driver_assignment.scalar_one_or_none()
            
            if not assignment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DriverAssignment not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(assignment, field, value)
            await db.commit()
            await db.refresh(assignment)
            return DriverAssignmentResponse(status="success", message="Driver unassigned", payload=assignment.to_dict())
        except HTTPException as e:
            return DriverAssignmentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverAssignmentResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_driver_assignment(self, db: AsyncSession, assignment_id: str, authorization: str = Header(...), **kwargs) -> DriverAssignmentResponse:
        """
        Delete a DriverAssignment assignment. Admin only.
        Args:
            db (AsyncSession): Database session
            assignment_id (str): DriverAssignment primary key
            authorization (str): Bearer token
        Returns:
            DriverAssignmentResponse
        """
        try:
            driver_assignment = await db.execute(select(DriverAssignment).where(DriverAssignment.assignment_id == assignment_id))
            assignment = driver_assignment.scalar_one_or_none()
            
            if not assignment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DriverAssignment not found")
            await db.delete(assignment)
            await db.commit()
            return DriverAssignmentResponse(status="success", message="DriverAssignment deleted successfully")
        except HTTPException as e:
            return DriverAssignmentResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverAssignmentResponse(status="error", message=str(e)).model_dump()
            )
