
from fastapi import FastAPI
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()
from .routers import pizza_routes, user_routes, order_routes, payment_routes
from .config.db import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("App is starting up...")
    
    create_tables()
    yield
    
    # Code to run on shutdown
    print("App is shutting down...")


app=FastAPI(lifespan=lifespan)


app.include_router(user_routes.router,tags=["Users"])
app.include_router(order_routes.router,tags=["Orders"])
app.include_router(pizza_routes.router,tags=["Pizzas"])
app.include_router(payment_routes.router,tags=["Payments"])



def start():
    import uvicorn
    uvicorn.run("deliverypizza.main:app", host="0.0.0.0", port=8080,reload=True)

    


