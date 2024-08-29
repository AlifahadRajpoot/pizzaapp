from typing import List
from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session,select
from deliverypizza.models.tables import Order, OrderItem, Pizza
from deliverypizza.models.schema import OrderUpdate
from deliverypizza.config.db import engine
from deliverypizza.security import get_current_user


router=APIRouter()


@router.post("/order",dependencies=[Depends(get_current_user)])
async def create_order(order:Order):
    with Session(engine) as session:        
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
        
    
@router.get("/order/{order_id}")
async def get_order(order_id:int):
    with Session(engine) as session:
        order=session.exec(select(Order).where(Order.id==order_id)).first()
        if not order:
            raise  HTTPException(status_code=404,detail="Order not found")
        return order
    
@router.get("/user/order/{user_id}")
async def get_user_order(user_id:int):
    with Session(engine) as session:
        order=session.exec(select(Order).where(Order.user_id==user_id)).all()
        if not order:
            raise  HTTPException(status_code=404,detail="Order not found")
        return order
    
@router.put("/ordre/{order_id}")
async def update_order(order_id:int,order:OrderUpdate):
    with Session(engine) as session:
        db_order=session.exec(select(Order).where(Order.id==order_id)).first()
        if not db_order:
            raise   HTTPException(status_code=404,detail="Order not found")
        order_data=order.model_dump(exclude_unset=True)
        db_order.sqlmodel_update(order_data)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return {"status":200,"Message":"Order Updated Successfully"}
    
@router.delete("/order/{order_id}")
async def delete_order(order_id:int):
    with Session(engine) as session:
        db_order=session.exec(select(Order).where(Order.id==order_id)).first()
        if not db_order:
            raise HTTPException(status_code=404,detail="Order not found")
        session.delete(db_order)
        session.commit()
        return {"status":200,"Message":"Order Deleted Successfully"}
    


    
        











