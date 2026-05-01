from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.routers.insurance_claim.insurance_claim_schemas import InsuranceClaimCreate, InsuranceClaimUpdate, InsuranceClaimResponse
from app.routers.insurance_claim.insurance_claim_controller import InsuranceClaimController

router = APIRouter(prefix="/insurance-claims", tags=["insurance-claims"])
controller = InsuranceClaimController()


@router.post("/create_claim", response_model=InsuranceClaimResponse)
async def create_insurance_claim(data: InsuranceClaimCreate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.create_insurance_claim(db=db, data=data, authorization=authorization)


@router.post("/get_all_claims", response_model=InsuranceClaimResponse)
async def get_all_insurance_claim(db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_all_insurance_claim(db=db, authorization=authorization)


@router.post("/get_claim/{claim_id}", response_model=InsuranceClaimResponse)
async def get_insurance_claim(claim_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.get_insurance_claim(db=db, claim_id=claim_id, authorization=authorization)


@router.post("/update_claim/{claim_id}", response_model=InsuranceClaimResponse)
async def update_insurance_claim(claim_id: str, data: InsuranceClaimUpdate, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.update_insurance_claim(db=db, claim_id=claim_id, data=data, authorization=authorization)


@router.post("/delete_claim/{claim_id}", response_model=InsuranceClaimResponse)
async def delete_insurance_claim(claim_id: str, db: AsyncSession = Depends(get_db), authorization: str = Header(...)):
    return await controller.delete_insurance_claim(db=db, claim_id=claim_id, authorization=authorization)
