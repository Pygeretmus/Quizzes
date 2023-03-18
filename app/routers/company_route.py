from core.connections           import get_db
from core.security              import get_current_user
from databases                  import Database
from fastapi                    import APIRouter, Depends
from schemas.company_schema     import *
from schemas.user_schema        import *
from services.company_service   import CompanyService


router = APIRouter()


@router.get('/companies', response_model=CompanyListResponse)
async def get_all_companies(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyListResponse:
    return await CompanyService(db=db).company_get_all()
 

@router.get('/company/{company_id}', response_model=CompanyResponse)
async def get_company_by_id(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db).company_get_id(company_id=company_id)


@router.delete('/company/{company_id}', response_model=dict)
async def delete_company_by_id(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> dict:
    return await CompanyService(db=db, user=user).company_delete(company_id=company_id)


@router.post('/company', response_model=CompanyResponse, status_code=201)
async def create_new_company(data:CompanyCreateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, user=user).company_create(data=data)


@router.put('/company/{company_id}', response_model=CompanyResponse)
async def upgrade_company(company_id: int, data:CompanyUpdateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, user=user).company_update(company_id=company_id, data=data)


@router.get('/company/{company_id}/members', response_model=MembersListResponse)
async def members_company(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MembersListResponse:
    return await CompanyService(db=db, user=user).company_members(company_id=company_id)


@router.delete("/company/{company_id}/member/{user_id}", response_model=MembersListResponse)
async def kick_member(company_id: int, user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MembersListResponse:
    return await CompanyService(db=db, user=user).member_kick(company_id=company_id, user_id=user_id)