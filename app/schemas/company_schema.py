from pydantic               import BaseModel
from typing                 import Optional



class Company(BaseModel):
    company_id: int
    company_name: str
    company_description: Optional[str] = ""
    company_owner_id: int
    
    class Config:
        orm_mode = True


class Companylist(BaseModel):
    companies: list[Company]


class CompanyCreateRequest(BaseModel):
    company_name: str = None
    company_description: Optional[str] = None


class CompanyUpdateRequest(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None


class CompanyResponse(BaseModel):
    result: Company


class CompanyListResponse(BaseModel):
    result: Companylist


class Member(BaseModel):
    user_id: int
    company_id: int


class MembersList(BaseModel):
    users: list[Member]


class MembersListResponse(BaseModel):
    result: MembersList