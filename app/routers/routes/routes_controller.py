from fastapi import HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.routers.routes.routes_model import Route
from app.routers.routes.routes_schemas import RouteCreate, RouteUpdate, RouteResponse
from app.config.core.middlewares import requires_auth, requires_admin


class RouteController:
    def __init__(self):
        pass

    @requires_admin
    async def create_routes(self, db: AsyncSession, data: RouteCreate, authorization: str = Header(...), **kwargs) -> RouteResponse:
        """
        Create a new Route route. Admin only.
        Args:
            db (AsyncSession): Database session
            data (RouteCreate): Route data
            authorization (str): Bearer token
        Returns:
            RouteResponse
        """
        try:
            route = Route(
                route_name=data.route_name,
                stop_order=data.stop_order,
                distance_km=data.distance_km,
                estimated_duration_min=data.estimated_duration_min,
                is_active=data.is_active if data.is_active is not None else True
            )
            
            db.add(route)
            await db.commit()
            await db.refresh(route)
            return RouteResponse(status="success", message="Route created successfully", payload=route.to_dict())
        except HTTPException as e:
            return RouteResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RouteResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_all_routes(self, db: AsyncSession, authorization: str = Header(...), **kwargs) -> RouteResponse:
        """
        Get all Route routes.
        Args:
            db (AsyncSession): Database session
            authorization (str): Bearer token
        Returns:
            RouteResponse
        """
        try:
            exiting_route = await db.execute(select(Route))
            routes = exiting_route.scalars().all()
            return RouteResponse(
                status="success",
                message="Routes retrieved successfully",
                payload=[r.to_dict() for r in routes]
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RouteResponse(status="error", message=str(e)).model_dump()
            )

    @requires_auth
    async def get_routes(self, db: AsyncSession, route_id: str, authorization: str = Header(...), **kwargs) -> RouteResponse:
        """
        Get a single Route by ID.
        Args:
            db (AsyncSession): Database session
            route_id (str): Route primary key
            authorization (str): Bearer token
        Returns:
            RouteResponse
        """
        try:
            exiting_route = await db.execute(select(Route).where(Route.route_id == route_id))
            route = exiting_route.scalar_one_or_none()
            if not route:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
            return RouteResponse(status="success", message="Route retrieved successfully", payload=route.to_dict())
        except HTTPException as e:
            return RouteResponse(status="error", message=e.detail)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RouteResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def update_routes(self, db: AsyncSession, route_id: str, data: RouteUpdate, authorization: str = Header(...), **kwargs) -> RouteResponse:
        """
        Update a Route route. Admin only.
        Args:
            db (AsyncSession): Database session
            route_id (str): Route primary key
            data (RouteUpdate): Fields to update
            authorization (str): Bearer token
        Returns:
            RouteResponse
        """
        try:
            exiting_route = await db.execute(select(Route).where(Route.route_id == route_id))
            route = exiting_route.scalar_one_or_none()
            if not route:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
            for field, value in data.model_dump(exclude_none=True).items():
                setattr(route, field, value)
            await db.commit()
            await db.refresh(route)
            return RouteResponse(status="success", message="Route updated successfully", payload=route.to_dict())
        except HTTPException as e:
            return RouteResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RouteResponse(status="error", message=str(e)).model_dump()
            )

    @requires_admin
    async def delete_routes(self, db: AsyncSession, route_id: str, authorization: str = Header(...), **kwargs) -> RouteResponse:
        """
        Delete a Route route. Admin only.
        Args:
            db (AsyncSession): Database session
            route_id (str): Route primary key
            authorization (str): Bearer token
        Returns:
            RouteResponse
        """
        try:
            exiting_route = await db.execute(select(Route).where(Route.route_id == route_id))
            route = exiting_route.scalar_one_or_none()
            if not route:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
            await db.delete(route)
            await db.commit()
            return RouteResponse(status="success", message="Route deleted successfully")
        except HTTPException as e:
            return RouteResponse(status="error", message=e.detail)
        except Exception as e:
            await db.rollback()
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=RouteResponse(status="error", message=str(e)).model_dump()
            )
