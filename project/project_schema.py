from typing import List
from pydantic import BaseModel

class ProjectDTO(BaseModel):
    memberid: str
    title: str
    sub_title : str
    project_type : List[str]
    project_category : str
    project_tag : str
    create_data : str
    link : str
    image : str


class TypeDTO(BaseModel):
    project_type : str