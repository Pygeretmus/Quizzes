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
    return await InviteService(db=db, user=user).invite_send(payload=payload)


@router.get("/my/", response_model=InviteListResponse)
async def my_invites(user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).invite_my_all()


@router.get("/company/{company_id}/", response_model=InviteListResponse)
async def company_invites(company_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> InviteListResponse:
    return await InviteService(db=db, user=user).invite_company_all(company_id=company_id)


@router.delete("/{invite_id}/", response_model=Response)
async def cancel_invite(invite_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> Response:
    return await InviteService(db=db, user=user).invite_cancel(invite_id=invite_id)


@router.get("/{invite_id}/accept/", response_model=Response)
async def accept_invite(invite_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> Response:
    return await InviteService(db=db, user=user).invite_accept(invite_id=invite_id)


@router.get("/{invite_id}/decline/", response_model=Response)
async def decline_invite(invite_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> Response:
    return await InviteService(db=db, user=user).invite_decline(invite_id=invite_id)