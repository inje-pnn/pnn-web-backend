from pydantic import BaseModel

class studyPostDTO(BaseModel):
    
    title: str
    user_id: str
    type: str
    content_link: str

class AccountPostDTO(BaseModel):

    account_id: str
    account_password: str
    sharer: str
    username: str