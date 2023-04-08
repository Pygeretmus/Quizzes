from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Companies, Members
from schemas.company_schema     import *
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select, insert, delete, update


class CompanyService:

    def __init__(self, db:Database, company_id: int = None, user: UserResponse = None):
        self.db = db
        self.user = user
        self.company_id = company_id


    async def company_get_all(self) -> CompanyListResponse:
        query = select(Companies)
        result = await self.db.fetch_all(query=query)
        return CompanyListResponse(detail="success", result = CompanyList(companies = [Company(**item) for item in result]))


    async def company_get_id(self) -> CompanyResponse:
        query = select(Companies).where(Companies.company_id == self.company_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
        return CompanyResponse(detail="success", result = Company(**result))


    async def owner_check(self) -> None:
        company = await self.company_get_id()
        if company.result.company_owner_id != self.user.result.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")


    async def company_delete(self) -> Response:
        await self.owner_check()
        query = delete(Companies).where(Companies.company_id == self.company_id)
        await self.db.execute(query=query)
        return Response(detail="success")


    async def company_create(self, data: CompanyCreateRequest) -> CompanyResponse:
        if not data.company_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name required")
        query = insert(Companies).values(
            company_name = data.company_name,
            company_description = data.company_description,
            company_owner_id = self.user.result.user_id
            ).returning(Companies)
        result = await self.db.fetch_one(query=query)
        await self.db.execute(query=insert(Members).values(user_id = self.user.result.user_id, company_id = result.company_id, role="owner"))
        return CompanyResponse(detail="success", result=Company(**result))


    async def make_changes(self, data: CompanyUpdateRequest) -> CompanyUpdateRequest:
        result = {}
        for items in data:
            if items[1]:
                result[items[0]] = items[1]
        return result
    

    async def company_update(self, data: CompanyUpdateRequest) -> CompanyResponse: 
        await self.owner_check()
        changes = await self.make_changes(data = data)
        if changes: 
            query = update(Companies).where(Companies.company_id == self.company_id).values(dict(changes))
            await self.db.execute(query=query)
        return await self.company_get_id()


    async def member_check(self) -> None:
        await self.company_get_id()
        query = select(Members).where(Members.company_id==self.company_id, Members.user_id == self.user.result.user_id)
        if not await self.db.fetch_one(query=query):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not member of this company")


    async def company_members(self) -> MembersListResponse:
        await self.member_check()
        query = select(Members).where(Members.company_id==self.company_id)
        result = await self.db.fetch_all(query=query)
        return MembersListResponse(detail="success", result=MembersList(users=[Member(**item) for item in result]))


    async def member_kick(self, user_id:int) -> Response:
        await self.owner_check()
        if self.user.result.user_id == user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't kick yourself")
        query = delete(Members).where(Members.company_id==self.company_id, Members.user_id == user_id)
        await self.db.execute(query=query)
        return Response(detail="success")


    async def company_admins(self) -> MembersListResponse:
        await self.member_check()
        query = select(Members).where(Members.company_id==self.company_id, Members.role=="admin")
        result = await self.db.fetch_all(query=query)
        return MembersListResponse(detail="success", result=MembersList(users=[Member(**item) for item in result]))        


    async def admin_downgrade(self, user_id:int) -> MemberResponse:
        await self.owner_check()
        query = update(Members).where(Members.company_id==self.company_id, Members.user_id == user_id).values(role="user").returning(Members)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user not a member of this company")
        return MemberResponse(detail="success", result=Member(**result))
    

    async def admin_upgrade(self, user_id:int) -> MemberResponse:
        await self.owner_check()
        query = update(Members).where(Members.company_id==self.company_id, Members.user_id == user_id).values(role="admin").returning(Members)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user not a member of this company")
        return MemberResponse(detail="success", result=Member(**result))
    

    async def ownership_give(self, user_id:int):
        await self.owner_check()
        if await self.db.fetch_one(query=update(Members).where(Members.company_id==self.company_id, Members.user_id==user_id, Members.role=="admin").values(role="owner").returning(Members)):
            await self.db.execute(query=update(Members).where(Members.company_id==self.company_id, Members.user_id==self.user.result.user_id, Members.role=="owner").values(role="admin"))
            await self.db.execute(query=update(Companies).where(Companies.company_id==self.company_id).values(company_owner_id=user_id))
            return Response(detail="success")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not admin")