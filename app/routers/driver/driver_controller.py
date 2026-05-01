from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.driver.driver_model import Driver
from app.routers.driver.driver_schemas import DriverCreate, DriverUpdate, DriverResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class DriverController:
    def __init__(self):
        pass

    @requires_admin
    async def create_driver(self, db: AsyncSession, data: DriverCreate, authorization: str = Header(...), **kwargs) -> DriverResponse:
        """
            Create a new Driver driver. Admin only.
            Args:
                db (AsyncSession): Database session
                data (DriverCreate): Driver data
                authorization (str): Bearer token
            Returns:
                DriverResponse
        """
        try:
            driver = Driver(
                name=data.name,
                license_number=data.license_number,
                phone=data.phone, 
                hire_date=data.hire_date,
                status=data.status
            )
            
            db.add(driver)
            await db.commit()
            await db.refresh(driver)
            return DriverResponse(status="success", message="Driver created successfully", payload=driver.to_dict())
        except HTTPException as e:
            return DriverResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_driver(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> DriverResponse:
        """
            Get all Driver drivers.
            Args:
                db (AsyncSession): Database session
                authorization (str): Bearer token
            Returns:
                DriverResponse
        """
        try:
            existing_drivers = await db.execute(select(Driver))
            drivers = existing_drivers.scalars().all()
            return DriverResponse(
                status="success",
                message="Drivers retrieved successfully",
                payload=[driver.to_dict() for driver in drivers]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_driver(self, db: AsyncSession, driver_id: str, authorization: str = Header(...), **kwargs) -> DriverResponse:
        """
            Get a single Driver by ID.
            Args:
                db (AsyncSession): Database session
                driver_id (str): Driver primary key
                authorization (str): Bearer token
            Returns:
                DriverResponse
        """
        try:
            exiting_driver = await db.execute(select(Driver).where(Driver.driver_id == driver_id))
            driver = exiting_driver.scalar_one_or_none()
            if not driver:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
            return DriverResponse(status="success", message="Driver retrieved successfully", payload=driver.to_dict())
        except HTTPException as e:
            return DriverResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_driver(self, db: AsyncSession, driver_id: str, data: DriverUpdate, authorization: str = Header(...), **kwargs) -> DriverResponse:
        """
            Update a Driver driver. Admin only.
            Args:
                db (AsyncSession): Database session
                driver_id (str): Driver primary key
                data (DriverUpdate): Fields to update
                authorization (str): Bearer token
            Returns:
                DriverResponse
        """
        try:
            exiting_driver = await db.execute(select(Driver).where(Driver.driver_id == driver_id))
            driver = exiting_driver.scalar_one_or_none()
            if not driver:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(driver, field, value)
            await db.commit()
            await db.refresh(driver)
            return DriverResponse(status="success", message="Driver updated successfully", payload=driver.to_dict())
        except HTTPException as e:
            return DriverResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_driver(self, db: AsyncSession, driver_id: str, authorization: str = Header(...), **kwargs) -> DriverResponse:
        """
            Delete a Driver driver. Admin only.
            Args:
                db (AsyncSession): Database session
                driver_id (str): Driver primary key
                authorization (str): Bearer token
            Returns:
                DriverResponse
        """
        try:
            exiting_driver = await db.execute(select(Driver).where(Driver.driver_id == driver_id))
            driver = exiting_driver.scalar_one_or_none()
            if not driver:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
            await db.delete(driver)
            await db.commit()
            return DriverResponse(status="success", message="Driver deleted successfully")
        except HTTPException as e:
            return DriverResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=DriverResponse(status="error", message=str(e)).model_dump()
            )
