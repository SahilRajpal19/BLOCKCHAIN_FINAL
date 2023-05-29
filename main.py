from fastapi import FastAPI
import uvicorn
import models
from router import blocks,users
from database import  engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine, checkfirst=True)


app.include_router(blocks.router)#including routers of blocks

# user_creation
app.include_router(users.router)# including routers of users



if __name__ == "__main__":
    uvicorn.run(app)
