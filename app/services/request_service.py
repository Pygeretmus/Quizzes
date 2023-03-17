from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Members, Requests
from schemas.company_schema     import *
from schemas.request_schema     import *
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select, insert, delete
from services.company_service   import CompanyService
from services.user_service      import UserService

class RequestService:

    def __init__(self, db:Database, user: UserResponse = None):
        self.db = db
        self.user = user


    async def send_request(self, payload: RequestCreateRequest) -> RequestResponse:
        await CompanyService(db=self.db).get_company_id(id=payload.to_company_id)
        if await self.db.fetch_one(query=select(Requests).where(Requests.from_user_id==self.user.result.user_id, Requests.to_company_id == payload.to_company_id)):
            raise HTTPException(status_code=400, detail="Request already sent")
        if await self.db.fetch_one(query=select(Members).where(Members.user_id==self.user.result.user_id, Members.company_id == payload.to_company_id)):
            raise HTTPException(status_code=400, detail="User is already a member of the company")
        query = insert(Requests).values(from_user_id = self.user.result.user_id, to_company_id = payload.to_company_id, request_message = payload.request_message)
        await self.db.execute(query=query)
        return RequestResponse(detail='success')
    

    async def my_requests(self) -> RequestListResponse:
        query = select(Requests).where(Requests.from_user_id==self.user.result.user_id)
        result = await self.db.fetch_all(query=query)
        return RequestListResponse(result=Requestlist(requests=[Request(**item) for item in result]))
    

    async def company_requests(self, company_id: int) -> RequestListResponse:
        await CompanyService(db=self.db, user=self.user).owner_check(id=company_id)
        query = select(Requests).where(Requests.to_company_id==company_id)
        result = await self.db.fetch_all(query=query)
        return RequestListResponse(result=Requestlist(requests=[Request(**item) for item in result]))


    async def get_request_id(self, request_id:int):
        query = select(Requests).where(Requests.request_id==request_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return result


    async def cancel_request(self, request_id: int) -> RequestResponse:
        request = await self.get_request_id(request_id=request_id)
        if request.from_user_id != self.user.result.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your request")
        query = delete(Requests).where(Requests.request_id==request_id)
        await self.db.execute(query=query)
        return RequestResponse(detail='success')
    

    async def check_request(self, request_id:int):
        request = await self.get_request_id(request_id=request_id)
        company = await CompanyService(user=self.user, db=self.db).get_company_id(id=request.to_company_id)
        if self.user.result.user_id != company.result.company_owner_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not your request")
        await self.db.execute(delete(Requests).where(Requests.request_id==request_id))
        return request


    async def accept_request(self, request_id: int) -> RequestResponse:
        request = await self.check_request(request_id=request_id)
        query = insert(Members).values(user_id = request.from_user_id, company_id = request.to_company_id)
        await self.db.execute(query=query)
        return RequestResponse(detail='success') 


    async def decline_request(self, request_id: int) -> RequestResponse:
        await self.check_request(request_id=request_id)
        return RequestResponse(detail='success') 