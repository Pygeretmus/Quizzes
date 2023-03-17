from core.connections           import get_db
from core.security              import get_current_user
from databases                  import Database
from fastapi                    import APIRouter, Depends
from schemas.invites_schema     import *
from schemas.user_schema        import UserResponse
from services.invite_service    import InviteService

router = APIRouter()


@router.post("/", response_model=InviteResponse)
async def invite_user(payload: InviteCreateRequest, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteResponse:
    return await InviteService(db=db, user=user).send_invite(payload=payload)


@router.get("/my", response_model=InviteListResponse)
async def invites_my(user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).my_invites()


@router.get("/company/{company_id}", response_model=InviteListResponse)
async def invites_company(company_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).company_invites(company_id=company_id)


@router.delete("/{invite_id}", response_model=InviteResponse)
async def invite_cancel(invite_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).cancel_invite(invite_id=invite_id)


@router.get("/{invite_id}/accept", response_model=InviteResponse)
async def invite_accept(invite_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).accept_invite(invite_id=invite_id)


@router.get("/{invite_id}/decline", response_model=InviteResponse)
async def invite_decline(invite_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).decline_invite(invite_id=invite_id)