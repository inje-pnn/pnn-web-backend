from pydantic import BaseModel
from typing import List

class studyPostDTO(BaseModel):
    
    title: str
    email: str
    project_type : List[str]
    project_category: str
    content_link: str
    description: str

class AccountPostDTO(BaseModel):

    account_id: str
    account_password: str
    sharer: str
    username: str