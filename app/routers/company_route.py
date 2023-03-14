from core.connections import get_db
from services.company_service import CompanyService
from databases import Database
from schemas.company_schema import *
from schemas.user_schema import *
from fastapi import APIRouter, Depends
from core.security import get_current_user


router = APIRouter()


@router.get('/companies', response_model=CompanyListResponse)
async def get_all_companies(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyListResponse:
    return await CompanyService(db=db).get_companies()
 

@router.get('/company/{company_id}', response_model=CompanyResponse)
async def get_company_by_id(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> UserResponse:
    return await CompanyService(db=db).get_company_id(id=company_id)


@router.delete('/company/{company_id}', response_model=str)
async def delete_company_id(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> str:
    return await CompanyService(db=db, user=user).delete_company(id=company_id)


@router.post('/company', response_model=CompanyResponse, status_code=201)
async def create_new_company(data:CompanyCreateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, user=user).create_company(data=data)


@router.put('/company/{company_id}', response_model=CompanyResponse)
async def upgrade_company(company_id: int, data:CompanyUpdateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, user=user).update_company(id=company_id, data=data)