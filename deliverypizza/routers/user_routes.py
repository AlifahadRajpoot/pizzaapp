
from datetime import timedelta
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session,select
from deliverypizza.config.db import engine
from deliverypizza.models.tables import User
from deliverypizza.models.schema import UserUpdate
from deliverypizza.security import authenticate_user, create_access_token, get_current_user, get_password_hash

router=APIRouter()

@router.post("/user/register")
async def register_user(user: User):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where((User.username == user.username) | (User.email == user.email))).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        user.password = get_password_hash(user.password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}

    
@router.put("/user/{user_id}")
async def update_user(user_id:int,user:UserUpdate):
    with Session(engine) as session:
        user_db=session.exec(select(User).where(User.id==user_id)).first()
        if not user_db:
            raise  HTTPException(status_code=404,detail="User not found")
        user_data=user.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(user_data)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return {"status":200,"Message":"User Udated Successfully"}
    
@router.delete("/user/{user_id}")
async def delete_user(user_id:int):
    with Session(engine) as session:
        user_db=session.exec(select(User).where(User.id==user_id)).first()
        if not user_db:
            raise  HTTPException(status_code=404,detail="User not found")
        session.delete(user_db)
        session.commit()
        return {"status":200,"Message":"User Deleted Successfully"}
    




        