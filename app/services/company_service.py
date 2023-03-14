from models.models import Companies
from schemas.company_schema import *
from schemas.user_schema import UserResponse
from sqlalchemy import select, insert, delete, update
from databases import Database
from fastapi import HTTPException, status
from services.user_service import UserService



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


    async def owner_check(self, id: int):
        company = await self.get_company_id(id=id)
        if self.user.result.user_id != company.result.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"It's not your company")


    async def get_companies(self) -> CompanyListResponse:
        query = select(Companies)
        result = await self.db.fetch_all(query=query)
        return CompanyListResponse(result = Companylist(companies = [Company(**item) for item in result]))


    async def get_company_id(self, id: int) -> CompanyResponse:
        query = select(Companies).where(Companies.company_id == id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company doesn't exist")
        return CompanyResponse(result = Company(**result))
    

    async def delete_company(self, id: int) -> str:
        await self.owner_check(id=id)
        query = delete(Companies).where(Companies.company_id == id)
        await self.db.execute(query=query)
        return "Successfully deleted"


    async def create_company(self, data: CompanyCreateRequest) -> CompanyResponse:
        if not data.company_name:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Name required")
        query = insert(Companies).values(
            company_name = data.company_name,
            company_description = data.company_description,
            company_owner_id = self.user.result.user_id
            ).returning(Companies)
        return CompanyResponse(result=await self.db.fetch_one(query=query))


    async def update_company(self, id: int, data: CompanyUpdateRequest) -> CompanyResponse: 
        await self.owner_check(id=id)
        changes = await self.make_changes(data = data)
        if changes: 
            query = update(Companies).where(Companies.company_id == id).values(dict(changes)).returning(Companies)
        return CompanyResponse(result=await self.db.fetch_one(query=query))
