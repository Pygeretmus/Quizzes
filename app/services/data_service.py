import csv

from aioredis.client            import Redis
from databases                  import Database
from fastapi                    import HTTPException, status
from fastapi.responses          import StreamingResponse
from io                         import StringIO, BytesIO
from models.models              import Members, Companies, Quizzes
from typing                     import Union
from schemas.quiz_schema        import Data, DataList, DataListResponse
from schemas.user_schema        import UserResponse
from sqlalchemy                 import select


class DataService:

    def __init__(self, redis:Redis, db:Database, company_id:int=None, user:UserResponse=None):
        self.db = db
        self.user = user
        self.redis = redis
        self.company_id = company_id


    async def attributes_check(self, company_id:int="*", quiz_id:int="*", user_id:int="*") -> None:
        if quiz_id != "*":
            quiz = await self.db.fetch_one(query=select(Quizzes).where(Quizzes.quiz_id == quiz_id))
            if not quiz:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This quiz not found")
        if company_id != "*":
            if not await self.db.fetch_one(query=select(Members).where(Members.company_id==company_id, Members.user_id==self.user.result.user_id)):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user not a member of this company")
            if quiz_id != "*":
                if quiz.company_id != company_id:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This quiz not in this company")
            if user_id != "*":
                if not await self.db.fetch_one(query=select(Members).where(Members.company_id==self.company_id, Members.user_id == user_id)):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not a member of this company")


    async def response_create(self, file:bool, keys:list) -> Union[DataListResponse, StreamingResponse]:
        if file:
            csv_buffer = StringIO()
            file_writer = csv.writer(csv_buffer)
            file_writer.writerow(["user", "company", "quiz", "attempt", "answer"])
            if keys:
                answers = [answer.decode('utf-8') for answer in await self.redis.mget(*keys)]
                # "company_2:user_3:quiz_1:attempt_1:question_1" into {'company':2,'user':3,'quiz':1,'attempt':1,'question':1}
                keys = [eval("{'" + key.decode('utf-8').replace(":", ",'").replace("_", "':") + "}") for key in keys]
                for counter, key in enumerate(keys):
                    file_writer.writerow([f'{key.get("user")}', f'{key.get("company")}', f'{key.get("quiz")}', f'{key.get("attempt")}', f'{answers[counter]}'])
            filename = BytesIO(csv_buffer.getvalue().encode())
            response = StreamingResponse(filename, media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=data.csv"
            return response
        if keys:    
            answers = [answer.decode('utf-8') for answer in await self.redis.mget(*keys)]
            keys = [eval("{'" + key.decode('utf-8').replace(":", ",'").replace("_", "':") + "}") for key in keys]
            for counter, key in enumerate(keys): 
                answers[counter] = Data(user_id=key.get("user"), 
                                        company_id=key.get("company"), 
                                        quiz_id=key.get("quiz"), 
                                        attempt=key.get("attempt"), 
                                        answer=answers[counter]) 
        else:
            answers = []
        return DataListResponse(detail="success", result=DataList(datas=answers))


    async def data_me(self, company_id:int="*", quiz_id:int="*", file=False) -> Union[DataListResponse, StreamingResponse]:
        await self.attributes_check(company_id=company_id, quiz_id=quiz_id)
        keys = await self.redis.keys(f'company_{company_id}:user_{self.user.result.user_id}:quiz_{quiz_id}:*')
        return await self.response_create(file=file, keys=keys)
        
     
    async def permission_check(self) -> None:
        query = select(Members).where(Members.company_id==self.company_id, Members.user_id==self.user.result.user_id).filter(Members.role.in_(["owner", "admin"]))
        if not await self.db.fetch_one(query=query):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesn't have permission for this")


    async def data_company(self, user_id:int="*", quiz_id:int="*", file=False) -> Union[DataListResponse, StreamingResponse]:
        await self.permission_check()
        await self.attributes_check(company_id=self.company_id, user_id=user_id, quiz_id=quiz_id)
        keys = await self.redis.keys(f'company_{self.company_id}:user_{user_id}:quiz_{quiz_id}:*')
        return await self.response_create(file=file, keys=keys)