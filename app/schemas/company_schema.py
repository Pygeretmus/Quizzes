from pydantic import BaseModel
from typing import Optional
from schemas.user_schema import User


class Company(BaseModel):
    company_id: int
    company_name: str
    company_description: Optional[str] = ""
    company_owner_id: int
    users: Optional[list[User]] = []

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
