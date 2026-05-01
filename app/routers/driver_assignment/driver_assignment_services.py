from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.driver_assignment.driver_assignment_schemas import DriverAssignmentCreate, DriverAssignmentUpdate, DriverAssignmentResponse
from app.routers.driver_assignment.driver_assignment_controller import DriverAssignmentController

router = APIRouter(prefix="/driver-assignments", tags=["driver-assignments"])
controller = DriverAssignmentController()


@router.post("/assign_driver", response_model=DriverAssignmentResponse)
async def create_driver_assignment(data: DriverAssignmentCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_driver_assignment(db=db, data=data, authorization=authorization)


@router.post("/get_all_assignments", response_model=DriverAssignmentResponse)
async def get_all_driver_assignment(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_driver_assignment(db=db, authorization=authorization)


@router.post("/get_assignment/{assignment_id}", response_model=DriverAssignmentResponse)
async def get_driver_assignment(assignment_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_driver_assignment(db=db, assignment_id=assignment_id, authorization=authorization)


@router.post("/update_assignment/{assignment_id}", response_model=DriverAssignmentResponse)
async def update_driver_assignment(assignment_id: str, data: DriverAssignmentUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_driver_assignment(db=db, assignment_id=assignment_id, data=data, authorization=authorization)


@router.post("/unassign_driver/{assignment_id}", response_model=DriverAssignmentResponse)
async def delete_driver_assignment(assignment_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_driver_assignment(db=db, assignment_id=assignment_id, authorization=authorization)
