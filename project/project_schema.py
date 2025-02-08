from pydantic import BaseModel

class ProjcetDTO(BaseModel):
    memberid: str
    title: str
    sub_title : str
    project_type : str
    project_category : str
    project_tag : str
    link : str
    image : str


class TypeDTO(BaseModel):
    project_type : str