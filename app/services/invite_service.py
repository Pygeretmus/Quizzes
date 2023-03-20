from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Invites, Members, Users, Companies
from schemas.company_schema     import *
from schemas.invites_schema     import *
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select, insert, delete


class InviteService:

    def __init__(self, db:Database, user: UserResponse = None):
        self.db = db
        self.user = user


    async def owner_check(self, company_id: int):
        query = select(Companies).where(Companies.company_id == company_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This company not found")
        if self.user.result.user_id != result.company_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your company")


    async def invite_send(self, payload: InviteCreateRequest) -> InviteResponse:
        await self.owner_check(company_id=payload.from_company_id)
        query = select(Users).where(Users.user_id == payload.to_user_id)
        if not await self.db.fetch_one(query=query):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not found")
        if await self.db.fetch_one(query=select(Invites).where(Invites.to_user_id==payload.to_user_id, Invites.from_company_id == payload.from_company_id)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite already exist")
        if await self.db.fetch_one(query=select(Members).where(Members.user_id==payload.to_user_id, Members.company_id == payload.from_company_id)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already in this company")
        query = insert(Invites).values(to_user_id = payload.to_user_id, from_company_id = payload.from_company_id, invite_message = payload.invite_message).returning(Invites)
        result = await self.db.fetch_one(query=query)
        return InviteResponse(detail='success', result=Invite(**result))
    

    async def invite_my_all(self) -> InviteListResponse:
        query = select(Invites).where(Invites.to_user_id==self.user.result.user_id)
        result = await self.db.fetch_all(query=query)
        return InviteListResponse(detail='success', result=InviteList(invites=[Invite(**item) for item in result]))
    

    async def invite_company_all(self, company_id: int) -> InviteListResponse:
        await self.owner_check(company_id=company_id)
        query = select(Invites).where(Invites.from_company_id==company_id)
        result = await self.db.fetch_all(query=query)
        return InviteListResponse(detail='success', result=InviteList(invites=[Invite(**item) for item in result]))


    async def get_invite_id(self, invite_id:int) -> InviteResponse:
        query = select(Invites).where(Invites.invite_id==invite_id)
        result = await self.db.fetch_one(query=query)
        if not result: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
        return InviteResponse(detail= "success", result=Invite(**result))


    async def invite_cancel(self, invite_id: int) -> Response:
        invite = await self.get_invite_id(invite_id=invite_id)
        await self.owner_check(company_id=invite.result.from_company_id)
        query = delete(Invites).where(Invites.invite_id==invite_id)
        await self.db.execute(query=query)
        return Response(detail="success")
    

    async def check_invite(self, invite_id:int) -> InviteResponse:
        invite = await self.get_invite_id(invite_id=invite_id)
        if invite.result.to_user_id != self.user.result.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your invite")
        await self.db.execute(delete(Invites).where(Invites.invite_id==invite_id))
        return invite


    async def invite_accept(self, invite_id: int) -> Response:
        invite = await self.check_invite(invite_id=invite_id)
        query = insert(Members).values(user_id = invite.result.to_user_id, company_id = invite.result.from_company_id, role="user")
        await self.db.execute(query=query)
        return Response(detail="success")


    async def invite_decline(self, invite_id: int) -> Response:
        await self.check_invite(invite_id=invite_id)
        return Response(detail="success")