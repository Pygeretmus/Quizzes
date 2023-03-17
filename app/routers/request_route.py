from core.connections           import get_db
from core.security              import get_current_user
from databases                  import Database
from fastapi                    import APIRouter, Depends
from schemas.request_schema     import *
from schemas.user_schema        import UserResponse
from services.request_service    import RequestService


router = APIRouter()


@router.post("/", response_model=RequestResponse)
async def request_company(payload: RequestCreateRequest, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> RequestResponse:
    return await RequestService(db=db, user=user).send_request(payload=payload)


@router.get("/my", response_model=RequestListResponse)
async def request_my(user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> RequestListResponse:
    return await RequestService(db=db, user=user).my_requests()


@router.get("/company/{company_id}", response_model=RequestListResponse)
async def requests_company(company_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> RequestListResponse:
    return await RequestService(db=db, user=user).company_requests(company_id=company_id)


@router.delete("/{request_id}", response_model=RequestResponse)
async def request_cancel(request_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> RequestListResponse:
    return await RequestService(db=db, user=user).cancel_request(request_id=request_id)


@router.get("/{request_id}/accept", response_model=RequestResponse)
async def request_accept(request_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> RequestListResponse:
    return await RequestService(db=db, user=user).accept_request(request_id=request_id)


@router.get("/{request_id}/decline", response_model=RequestResponse)
async def request_decline(request_id: int, user:UserResponse=Depends(get_current_user), db:Database=Depends(get_db)) -> RequestListResponse:
    return await RequestService(db=db, user=user).decline_request(request_id=request_id)