from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemes, crud, database

users_router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@users_router.post("/", response_model=schemes.User)
def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)) -> schemes.User:
    user_crud = crud.UserCRUD(db=db)
    db_user = user_crud.get_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User with email={user.email} already exists")

    db_user = user_crud.create_user(user=user)
    return db_user

@users_router.get("/{user_id}", response_model=schemes.User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> schemes.User:
    user_crud = crud.UserCRUD(db=db)
    db_user = user_crud.get(user_id)
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail=f"User with ID={user_id} not found")

@users_router.put("/{user_id}", response_model=schemes.User)
def update_user(user_id: int, user_update: schemes.UserBase, db: Session = Depends(get_db)) -> schemes.User:
    user_crud = crud.UserCRUD(db=db)
    db_user = user_crud.get_by_id(user_id=user_id)

    if db_user:
        updated_user = user_crud.update(user_id=db_user.id, user_data=user_update)
        return updated_user
    else:
        raise HTTPException(status_code=404, detail=f"User with ID={user_id} not found")

@users_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict:
    user_crud = crud.UserCRUD(db=db)
    db_user = user_crud.get(user_id)
    if db_user:
        user_crud.delete(user_id=db_user.id)
        return {"detail": "User deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"User with ID={user_id} not found")

