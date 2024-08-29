from fastapi import APIRouter,HTTPException
from sqlmodel import Session,select
from deliverypizza.models.tables import Payment
from deliverypizza.models.schema import PaymentUpdate
from deliverypizza.config.db import  engine


router=APIRouter()


@router.post("/payment")
async def create_payment(payment:Payment):
    with Session(engine) as session:
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment
    
@router.get("/payment/{payment_id}")
async def get_payment(payment_id:int):
    with Session(engine) as session:
        payment=session.exec(select(Payment).where(Payment.id==payment_id)).first()
        if not payment:
            raise  HTTPException(status_code=404,detail="Payment not found")
        return payment
    
@router.get("/order/payment/{order_id}")
async def get_order_payment(order_id:int):
    with Session(engine) as session:
        payment=session.exec(select(Payment).where(Payment.order_id==order_id)).all()
        if not payment:
            raise  HTTPException(status_code=404,detail="Payment not found")
        return payment
    
@router.put("/payment/{payment_id}")
async def update_payment(payment_id:int,payment:PaymentUpdate):
    with Session(engine) as session:
        db_payment=session.exec(select(Payment).where(Payment.id==payment_id)).first()
        if not db_payment:
            raise   HTTPException(status_code=404,detail="Payment not found")
        payment_data=payment.model_dump(exclude_unset=True)
        db_payment.sqlmodel_update(payment_data)
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)
        return {"status":200,"Message":"Payment Updated Successfully"}
    
@router.delete("/payment/{payment_id}")
async def delete_payment(payment_id:int):
    with Session(engine) as session:
        db_payment=session.exec(select(Payment).where(Payment.id==payment_id)).first()
        if not db_payment:
            raise HTTPException(status_code=404,detail="Payment not found")
        session.delete(db_payment)
        session.commit()
        return {"status":200,"Message":"Payment Deleted Successfully"}
    