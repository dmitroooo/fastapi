from fastapi import FastAPI
from typing import List
import sqlalchemy
import databases
import datetime, uuid

from passlib.context import CryptContext
from pydantic import BaseModel

from models.product_model import ProductList, ProductDelete, ProductEntry, ProductUpdate
from models.users_model import UserList, UserEntry, UserUpdate, UserDelete
from models.posts_model import PostList, PostEntry, PostUpdate, PostDelete


DATABASE_URL = "postgresql://riwhsptnyormqw:4968cefd626fdb958741475384c319b99d3628734b182c9c2f50077a2f87d4e5@ec2-3-248-87-6.eu-west-1.compute.amazonaws.com:5432/d4q71til8sh0an"
database = databases.Database(DATABASE_URL)



metadata = sqlalchemy.MetaData()



#PRODUCT

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
   
)


users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("gender", sqlalchemy.CHAR  ),
    sqlalchemy.Column("create_at", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.CHAR  ),
)

groups = sqlalchemy.Table(
    "group",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
)

posts = sqlalchemy.Table(
    "post",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("create_at", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(
    docs_url="/",
    redoc_url="/redocs",
    title="Fart-API postgreSQL",
    description="Привeт",
    version="1.4.8.8",
    openapi_url="/api/v2/openapi.json",  
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()





#USERS
@app.get("/users", response_model=List[UserList], tags=["Users"])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users", response_model=UserList, tags=["Users"])
async def register_user(user: UserEntry):
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username   = user.username,
        password   = pwd_context.hash(user.password),
        first_name = user.first_name,
        last_name  = user.last_name,
        gender     = user.gender,
        create_at  = gDate,
        status     = "1"
    ) 
    await database.execute(query)
    return {
        "id": gID,
        **user.dict(),
        "create_at":gDate,
        "status": "1"
    }


@app.get("/users/{userId}", response_model=UserList, tags=["Users"])
async def find_user_by_id(userId: str):
    query = users.select().where(users.c.id == userId)
    return await database.fetch_one(query)



@app.put("/users", response_model=UserList, tags=["Users"])
async def update_user(user: UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name  = user.last_name,
            gender     = user.gender,
            status     = user.status,
            create_at  = gDate,
        )
    await database.execute(query)

    return await find_user_by_id(user.id)



@app.delete("/users/{userId}", tags=["Users"])
async def delete_user(user: UserDelete):
    query = users.delete().where(users.c.id == user.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This user has been deleted successfully." 
    }




@app.get("/product", response_model=List[ProductList], tags=["Products"])

async def find_all_products():
    query = products.select()
    return await database.fetch_all(query)

@app.post("/prosucts", response_model=ProductList, tags=["Products"])
async def register_product(product: ProductEntry):
    gID   = str(uuid.uuid1())
    query = products.insert().values(
        id = gID,
        name   = product.name,
        price = product.price,
    ) 
    await database.execute(query)
    return {
        "id": gID,
        **product.dict()
    }

@app.get("/products/{productId}", response_model=ProductList, tags=["Products"])
async def find_product_by_id(productId: str):
    query = products.select().where(products.c.id == productId)
    return await database.fetch_one(query)

@app.put("/products", response_model=ProductList, tags=["Products"])
async def update_productr(product: ProductUpdate):
    query = products.update().\
        where(products.c.id == product.id).\
        values(
            name = product.name,
            price  = product.price,
        )
    await database.execute(query)

    return await find_product_by_id(product.id)

@app.delete("/products/{productId}", tags=["Products"])
async def delete_product(product: ProductDelete):
    query = products.delete().where(products.c.id == product.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This product has been deleted successfully." 
    }


#POST
@app.get("/post", response_model=List[PostList], tags=["Posts"])
async def find_all_posts():
    query = posts.select()
    return await database.fetch_all(query)



@app.post("/post", response_model=PostList, tags=["Posts"])
async def register_post(post: PostEntry):
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = posts.insert().values(
        id = gID,
        title   = post.title,
        description   = post.description,
        create_at  = gDate,
    ) 
    await database.execute(query)
    return {
        "id": gID,
        **post.dict()
    }


@app.get("/post/{postId}", response_model=PostList, tags=["Posts"])
async def find_post_by_id(postId: str):
    query = posts.select().where(posts.c.id == postId)
    return await database.fetch_one(query)



@app.put("/posts", response_model=PostList, tags=["Posts"])
async def update_post(post: PostUpdate):
    gDate = str(datetime.datetime.now())
    query = posts.update().\
        where(posts.c.id == post.id).\
        values(
            title = post.title,
            description  = post.description,
            create_at  = gDate,
        )
    await database.execute(query)

    return await find_post_by_id(post.id)



@app.delete("/post/{postId}", tags=["Posts"])
async def delete_post(post: PostDelete):
    query = post.delete().where(posts.c.id == post.id)
    await database.execute(query)

    return {
        "status" : True,
        "message": "This post has been deleted successfully." 
    }
