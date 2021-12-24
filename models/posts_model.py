from pydantic import BaseModel, Field

## Models
class PostList(BaseModel):
    id           : str
    title        : str
    description  : str
    create_at    : str
class PostEntry(BaseModel):
    title        : str = Field(..., example="NEW funny post")
    description  : str = Field(..., example="description post bla bla bla")
class PostUpdate(BaseModel):
    id           : str = Field(..., example="Enter post id")
    title        : str = Field(..., example="Updated funny post")
    description  : str = Field(..., example="Updated description bla bla bla Updated")

class PostDelete(BaseModel):
    id: str = Field(..., example="Enter post id")