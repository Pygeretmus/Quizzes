from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Companies, Members
from schemas.company_schema     import *
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select, insert, delete, update


class CompanyService:

    def __init__(self, db:Database, user: UserResponse = None):
        self.db = db
        self.user = user


    async def make_changes(self, data: CompanyUpdateRequest) -> CompanyUpdateRequest:
        result = {}
        for items in data:
            if items[1]:
                result[items[0]] = items[1]
        return result


    async def owner_check(self, company_id: int):
        company = await self.company_get_id(company_id=company_id)
        if self.user.result.user_id != company.result.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")


    async def company_get_all(self) -> CompanyListResponse:
        query = select(Companies)
        result = await self.db.fetch_all(query=query)
        return CompanyListResponse(detail="success", result = CompanyList(companies = [Company(**item) for item in result]))


    async def company_get_id(self, company_id: int) -> CompanyResponse:
        query = select(Companies).where(Companies.company_id == company_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
        return CompanyResponse(detail="success", result = Company(**result))
    

    async def company_delete(self, company_id: int) -> dict:
        await self.owner_check(company_id=company_id)
        query = delete(Companies).where(Companies.company_id == company_id)
        await self.db.execute(query=query)
        return {"detail": "success"}


    async def company_create(self, data: CompanyCreateRequest) -> CompanyResponse:
        if not data.company_name:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Name required")
        query = insert(Companies).values(
            company_name = data.company_name,
            company_description = data.company_description,
            company_owner_id = self.user.result.user_id
            ).returning(Companies)
        result = await self.db.fetch_one(query=query)
        await self.db.execute(query=insert(Members).values(user_id = self.user.result.user_id, company_id = result.company_id))
        return CompanyResponse(detail="success", result=Company(**result))


    async def company_update(self, company_id: int, data: CompanyUpdateRequest) -> CompanyResponse: 
        await self.owner_check(company_id=company_id)
        changes = await self.make_changes(data = data)
        if changes: 
            query = update(Companies).where(Companies.company_id == company_id).values(dict(changes)).returning(Companies)
        result = await self.db.fetch_one(query=query)
        return CompanyResponse(detail="success", result=Company(**result))
    

    async def company_members(self, company_id: int) -> MembersListResponse: 
        await self.owner_check(company_id=company_id)
        query = select(Members).where(Members.company_id==company_id)
        result = await self.db.fetch_all(query=query)
        return MembersListResponse(detail="success", result=MembersList(users=[Member(**item) for item in result]))
    

    async def member_kick(self, company_id:int, user_id:int) -> MembersListResponse:
        await self.owner_check(company_id=company_id)
        query = delete(Members).where(Members.company_id==company_id, Members.user_id == user_id)
        await self.db.fetch_all(query=query)
        return await self.company_members(company_id=company_id)