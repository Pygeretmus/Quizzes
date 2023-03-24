from core.connections           import get_db
from core.security              import get_current_user
from databases                  import Database
from fastapi                    import APIRouter, Depends
from schemas.company_schema     import *
from schemas.user_schema        import UserResponse
from services.company_service   import CompanyService


router = APIRouter()


@router.get('/companies/', response_model=CompanyListResponse)
async def get_all_companies(user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyListResponse:
    return await CompanyService(db=db).company_get_all()
 

@router.get('/company/{company_id}/', response_model=CompanyResponse)
async def get_company_by_id(company_id:int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, company_id=company_id).company_get_id()


@router.delete('/company/{company_id}/', response_model=Response)
async def delete_company_by_id(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> Response:
    return await CompanyService(db=db, user=user, company_id=company_id).company_delete()


@router.post('/company/', response_model=CompanyResponse, status_code=201)
async def create_new_company(data:CompanyCreateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, user=user).company_create(data=data)


@router.put('/company/{company_id}/', response_model=CompanyResponse)
async def upgrade_company(company_id: int, data:CompanyUpdateRequest, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> CompanyResponse:
    return await CompanyService(db=db, user=user, company_id=company_id).company_update(data=data)


@router.get('/company/{company_id}/members/', response_model=MembersListResponse)
async def members_company(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MembersListResponse:
    return await CompanyService(db=db, user=user, company_id=company_id).company_members()


@router.delete("/company/{company_id}/member/{user_id}/", response_model=Response)
async def kick_member(company_id: int, user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> Response:
    return await CompanyService(db=db, user=user, company_id=company_id).member_kick(user_id=user_id)


@router.get("/company/{company_id}/admins/", response_model=MembersListResponse)
async def admins_company(company_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MembersListResponse:
    return await CompanyService(db=db, user=user, company_id=company_id).company_admins()


@router.delete("/company/{company_id}/admin/{user_id}/", response_model=MemberResponse)
async def downgrade_admin(company_id: int, user_id: int, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MemberResponse:
    return await CompanyService(db=db, user=user, company_id=company_id).admin_downgrade(user_id=user_id)


@router.post("/company/{company_id}/admin/", response_model=MemberResponse)
async def upgrade_admin(company_id: int, payload:AdminUpgrade, user: UserResponse = Depends(get_current_user), db: Database = Depends(get_db)) -> MemberResponse:
    return await CompanyService(db=db, user=user, company_id=company_id).admin_upgrade(user_id=payload.user_id)