from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.vehicle.vehicle_model import Vehicle
from app.routers.vehicle.vehicle_schemas import VehicleCreate, VehicleUpdate, VehicleResponse
from app.routers.core.middlewares import requires_auth, requires_admin


class VehicleController:
    def __init__(self):
        pass

    @requires_admin
    async def create_vehicle(self, db: AsyncSession, vehicle_create: VehicleCreate, authorization: str = Header(...), **kwargs) -> VehicleResponse:
        try:
            existing = await db.execute(select(Vehicle).where(Vehicle.registration_number == vehicle_create.registration_number))
            if existing.scalar():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle with this registration number already exists")

            vehicle = Vehicle(
                registration_number=vehicle_create.registration_number,
                model=vehicle_create.model,
                capacity=vehicle_create.capacity,
                status=vehicle_create.status,
                purchase_date=vehicle_create.purchase_date,  
                license_expiry=vehicle_create.license_expiry 
            )
            
            db.add(vehicle)
            await db.commit()
            await db.refresh(vehicle)

            return VehicleResponse(status="success", message="Vehicle created successfully", payload=vehicle.to_dict())

        except HTTPException as e:
            return VehicleResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=VehicleResponse(status="error", message=str(e)).model_dump())

    @requires_admin
    async def get_all_vehicles(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> VehicleResponse:
        try:
            result = await db.execute(select(Vehicle))
            vehicles = result.scalars().all()

            return VehicleResponse(status="success", message="Vehicles retrieved successfully", payload=[v.to_dict() for v in vehicles])

        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=VehicleResponse(status="error", message=str(e)).model_dump())

    @requires_auth
    async def get_vehicle(self, db: AsyncSession, vehicle_id: str, authorization: str = Header(...), **kwargs) -> VehicleResponse:
        try:
            result = await db.execute(select(Vehicle).where(Vehicle.vehicle_id == vehicle_id))
            vehicle = result.scalar_one_or_none()

            if not vehicle:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

            return VehicleResponse(status="success", message="Vehicle retrieved successfully", payload=vehicle.to_dict())

        except HTTPException as e:
            return VehicleResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=VehicleResponse(status="error", message=str(e)).model_dump())

    @requires_admin
    async def update_vehicle(self, db: AsyncSession, vehicle_id: str, vehicle_update: VehicleUpdate, authorization: str = Header(...), **kwargs) -> VehicleResponse:
        try:
            result = await db.execute(select(Vehicle).where(Vehicle.vehicle_id == vehicle_id))
            vehicle = result.scalar_one_or_none()

            if not vehicle:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

            for field, value in vehicle_update.model_dump(exclude_none=True).items():
                setattr(vehicle, field, value)

            await db.commit()
            await db.refresh(vehicle)

            return VehicleResponse(status="success", message="Vehicle updated successfully", payload=vehicle.to_dict())

        except HTTPException as e:
            return VehicleResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=VehicleResponse(status="error", message=str(e)).model_dump())

    @requires_admin
    async def delete_vehicle(self, db: AsyncSession, vehicle_id: str, authorization: str = Header(...), **kwargs) -> VehicleResponse:
        try:
            result = await db.execute(select(Vehicle).where(Vehicle.vehicle_id == vehicle_id))
            vehicle = result.scalar_one_or_none()

            if not vehicle:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")

            await db.delete(vehicle)
            await db.commit()

            return VehicleResponse(status="success", message="Vehicle deleted successfully")

        except HTTPException as e:
            return VehicleResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=VehicleResponse(status="error", message=str(e)).model_dump())