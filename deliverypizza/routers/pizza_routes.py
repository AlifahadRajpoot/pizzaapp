from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session,select
from deliverypizza.config.db import  engine
from deliverypizza.models.tables import Pizza
from deliverypizza.models.schema import PizzaUpdate
from typing import List

from deliverypizza.security import get_current_user

router=APIRouter()

@router.post("/pizza",dependencies=[Depends(get_current_user)])
async def create_pizza(pizza:Pizza):
    new_pizza = Pizza(
        name=pizza.name,
        size=pizza.size,
        quantity=pizza.quantity,
        price=pizza.price
    )
    
    with Session(engine) as session:
        session.add(new_pizza)
        session.commit()
        session.refresh(new_pizza)
        return new_pizza

@router.get("/pizza",response_model=List[Pizza])
async def read_pizzas():
    with Session(engine) as session:
        pizza=session.exec(select(Pizza).where(Pizza.is_available==True)).all()
        return pizza
    
@router.get("/pizza/{pizza_id}")
async def read_pizza(pizza_id: int):
    with Session(engine) as session:
        pizza=session.exec(select(Pizza).where(Pizza.id==pizza_id)).first()
        if not pizza:
            raise HTTPException(status_code=404,detail="Pizza not found")
        return pizza
    
@router.put("/pizza/{pizza_id}")
async def update_pizza(pizza_id: int,pizza:PizzaUpdate):
    with Session(engine) as session:
        db_pizza=session.exec(select(Pizza).where(Pizza.id==pizza_id)).first()
        if  not db_pizza:
            raise HTTPException(status_code=404,detail="Pizza not found")
        pizza_data=pizza.model_dump(exclude_unset=True)
        db_pizza.sqlmodel_update(pizza_data)
        session.add(db_pizza)
        session.commit()
        session.refresh(db_pizza)
        return {"status":200,"Message":"Pizza Updated Successfully"}
    
@router.delete("/pizza/{pizza_id}")
async def delete_pizza(pizza_id: int):
    with Session(engine) as session:
        db_pizza=session.exec(select(Pizza).where(Pizza.id==pizza_id)).first()
        if not db_pizza:
            raise  HTTPException(status_code=404,detail="Pizza not found")
        session.delete(db_pizza)
        session.commit()
        return {"status":200,"Message":"Pizza Deleted Successfully"}




        






            


    

