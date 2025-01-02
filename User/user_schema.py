from pydantic import BaseModel

class ExampleDTO(BaseModel):
    name: str
    age: int