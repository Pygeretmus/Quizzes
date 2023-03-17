from databases                  import Database
from fastapi                    import HTTPException, status
from models.models              import Invites, Members
from schemas.company_schema     import *
from schemas.invites_schema     import *
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select, insert, delete
from services.company_service   import CompanyService
from services.user_service      import UserService

class InviteService:

    def __init__(self, db:Database, user: UserResponse = None):
        self.db = db
        self.user = user


    async def send_invite(self, payload: InviteCreateRequest) -> InviteResponse:
        await UserService(db=self.db).get_user_id(id=payload.to_user_id)
        await CompanyService(db=self.db, user=self.user).owner_check(id=payload.from_company_id)
        if await self.db.fetch_one(query=select(Invites).where(Invites.to_user_id==payload.to_user_id, Invites.from_company_id == payload.from_company_id)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invite already exist")
        if await self.db.fetch_one(query=select(Members).where(Members.user_id==payload.to_user_id, Members.company_id == payload.from_company_id)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already in this company")
        query = insert(Invites).values(to_user_id = payload.to_user_id, from_company_id = payload.from_company_id, invite_message = payload.invite_message)
        await self.db.execute(query=query)
        return InviteResponse(detail='success')
    

    async def my_invites(self) -> InviteListResponse:
        query = select(Invites).where(Invites.to_user_id==self.user.result.user_id)
        result = await self.db.fetch_all(query=query)
        return InviteListResponse(result=Invitelist(invites=[Invite(**item) for item in result]))
    

    async def company_invites(self, company_id: int) -> InviteListResponse:
        await CompanyService(db=self.db, user=self.user).owner_check(id=company_id)
        query = select(Invites).where(Invites.from_company_id==company_id)
        result = await self.db.fetch_all(query=query)
        return InviteListResponse(result=Invitelist(invites=[Invite(**item) for item in result]))


    async def get_invite_id(self, invite_id:int):
        query = select(Invites).where(Invites.invite_id==invite_id)
        result = await self.db.fetch_one(query=query)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invite not found")
        return result


    async def cancel_invite(self, invite_id: int) -> InviteResponse:
        invite = await self.get_invite_id(invite_id=invite_id)
        await CompanyService(db=self.db, user=self.user).owner_check(id=invite.from_company_id)
        query = delete(Invites).where(Invites.invite_id==invite_id)
        await self.db.execute(query=query)
        return InviteResponse(detail='success')
    

    async def check_invite(self, invite_id:int):
        invite = await self.get_invite_id(invite_id=invite_id)
        if invite.to_user_id != self.user.result.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="It is not your invite")
        await self.db.execute(delete(Invites).where(Invites.invite_id==invite_id))
        return invite


    async def accept_invite(self, invite_id: int) -> InviteResponse:
        invite = await self.check_invite(invite_id=invite_id)
        query = insert(Members).values(user_id = invite.to_user_id, company_id = invite.from_company_id)
        await self.db.execute(query=query)
        return InviteResponse(detail='success') 


    async def decline_invite(self, invite_id: int) -> InviteResponse:
        await self.check_invite(invite_id=invite_id)
        return InviteResponse(detail='success') 