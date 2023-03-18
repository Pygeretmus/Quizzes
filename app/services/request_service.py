from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Members, Requests, Users, Companies
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

    
    async def company_get_id(self, company_id: int) -> CompanyResponse:
        query = select(Companies).where(Companies.company_id == company_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
        return CompanyResponse(detail="success", result = Company(**result))


    async def request_send(self, payload: RequestCreateRequest) -> RequestResponse:
        await self.company_get_id(company_id=payload.to_company_id)
        if await self.db.fetch_one(query=select(Requests).where(Requests.from_user_id==self.user.result.user_id, Requests.to_company_id == payload.to_company_id)):
            raise HTTPException(status_code=400, detail="Request already sent")
        if await self.db.fetch_one(query=select(Members).where(Members.user_id==self.user.result.user_id, Members.company_id == payload.to_company_id)):
            raise HTTPException(status_code=400, detail="User is already a member of the company")
        query = insert(Requests).values(from_user_id = self.user.result.user_id, to_company_id = payload.to_company_id, request_message = payload.request_message).returning(Requests)
        result = await self.db.fetch_one(query=query)
        return RequestResponse(detail='success', result=Request(**result))
    

    async def request_my_all(self) -> RequestListResponse:
        query = select(Requests).where(Requests.from_user_id==self.user.result.user_id)
        result = await self.db.fetch_all(query=query)
        return RequestListResponse(detail='success', result=RequestList(requests=[Request(**item) for item in result]))
    

    async def request_company_all(self, company_id: int) -> RequestListResponse:
        query = select(Companies).where(Companies.company_id == company_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
        if self.user.result.user_id != result.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")
        query = select(Requests).where(Requests.to_company_id==company_id)
        result = await self.db.fetch_all(query=query)
        return RequestListResponse(detail='success', result=RequestList(requests=[Request(**item) for item in result]))


    async def request_get_id(self, request_id:int) -> RequestResponse:
        query = select(Requests).where(Requests.request_id==request_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return RequestResponse(detail="success", result=Request(**result))


    async def request_cancel(self, request_id: int) -> RequestListResponse:
        request = await self.request_get_id(request_id=request_id)
        if request.result.from_user_id != self.user.result.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your request")
        query = delete(Requests).where(Requests.request_id==request_id)
        await self.db.execute(query=query)
        return await self.request_my_all() 


    async def request_check(self, request_id:int) -> RequestResponse:
        request = await self.request_get_id(request_id=request_id)
        company = await self.company_get_id(company_id=request.result.to_company_id)
        if self.user.result.user_id != company.result.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your's company request")
        await self.db.execute(delete(Requests).where(Requests.request_id==request_id))
        return request


    async def request_accept(self, request_id: int) -> dict:
        request = await self.request_check(request_id=request_id)
        query = insert(Members).values(user_id = request.result.from_user_id, company_id = request.result.to_company_id)
        await self.db.execute(query=query)
        return {"detail":"success"} 


    async def request_decline(self, request_id: int) -> dict:
        await self.request_check(request_id=request_id)
        return {"detail":"success"} 