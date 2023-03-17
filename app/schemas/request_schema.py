from pydantic import BaseModel


class Request(BaseModel):
    request_id : int
    to_company_id : int
    from_user_id : int
    request_message: str

    class Config:
        orm_mode = True


class Requestlist(BaseModel):
    requests: list[Request]


class RequestCreateRequest(BaseModel):
    to_company_id : int
    request_message: str


class RequestResponse(BaseModel):
    detail: str


class RequestListResponse(BaseModel):
    result: Requestlist