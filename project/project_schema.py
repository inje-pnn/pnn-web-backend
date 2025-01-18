from pydantic import BaseModel

class ProjcetDTO(BaseModel):
    memberid: str
    title: str
    postdate : str
    project_type : str
    link : str
    add_content : str
    image : str


class TypeDTO(BaseModel):
    project_type : str