from pydantic import BaseModel, Field
class ProductList(BaseModel):
    id : str
    name: str
    price: int

class ProductEntry(BaseModel):
    name: str = Field(..., example="ogurec")
    price: int  = Field(..., example="100")

class ProductUpdate(BaseModel):
    id           : str = Field(..., example="Enter your id")
    name         : str = Field(..., example="NameProduct")
    price        : int = Field(..., example="200")

class ProductDelete(BaseModel): 
    id: str = Field(..., example="Enter your id")

