from pydantic import BaseModel


class Invite(BaseModel):
    invite_id: int
    to_user_id: int
    from_company_id: int
    invite_message: str

    class Config:
        orm_mode = True


class InviteList(BaseModel):
    invites: list[Invite]


class InviteCreateRequest(BaseModel):
    to_user_id: int
    from_company_id: int
    invite_message: str


class Response(BaseModel):
    detail: str


class InviteResponse(Response):
    result: Invite


class InviteListResponse(Response):
    result: InviteList