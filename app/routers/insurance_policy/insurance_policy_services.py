from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.insurance_policy.insurance_policy_schemas import InsurancePolicyCreate, InsurancePolicyUpdate, InsurancePolicyResponse
from app.routers.insurance_policy.insurance_policy_controller import InsurancePolicyController

router = APIRouter(prefix="/insurance-policies", tags=["insurance-policies"])
controller = InsurancePolicyController()


@router.post("/add_insurance_policy", response_model=InsurancePolicyResponse)
async def create_insurance_policy(data: InsurancePolicyCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_insurance_policy(db=db, data=data, authorization=authorization)


@router.post("/get_all_insurance_policies", response_model=InsurancePolicyResponse)
async def get_all_insurance_policy(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_insurance_policy(db=db, authorization=authorization)


@router.post("/get_insurance_policy/{insurance_id}", response_model=InsurancePolicyResponse)
async def get_insurance_policy(insurance_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_insurance_policy(db=db, insurance_id=insurance_id, authorization=authorization)


@router.post("/update_insurance_policy/{insurance_id}", response_model=InsurancePolicyResponse)
async def update_insurance_policy(insurance_id: str, data: InsurancePolicyUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_insurance_policy(db=db, insurance_id=insurance_id, data=data, authorization=authorization)


@router.post("/delete_insurance_policy/{insurance_id}", response_model=InsurancePolicyResponse)
async def delete_insurance_policy(insurance_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_insurance_policy(db=db, insurance_id=insurance_id, authorization=authorization)
