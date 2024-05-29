from typing import Union, Optional
from app import models
from app import schemes
from typing import Optional
from sqlalchemy.orm import Session
import hashlib
from app import database

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()

    def create_user(self, user: schemes.UserCreate):
        hashed_password = hashlib.md5(user.password.encode()).hexdigest()
        db_user = models.User(
            email=user.email,
            first_name=user.first_name,
            second_name=user.second_name,
            password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_id(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def update(self, user_id: int, user_data: schemes.UserBase):
        db_user = self.get_by_id(user_id)
        if db_user:
            for key, value in user_data.dict().items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user

    def delete(self, user_id: int):
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()

class Record_crud():
    def __init__(self, db: Session):
        self.db = db

    def create(self, record: schemes.RecordCreate) -> schemes.Record:
        db_record = models.Record(date=record.date, title=record.title,
                                  content=record.content)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def create_record_connected_to_user(self, db_record: models.Record, user_id: int) -> models.Record:
        db_record.user_id = user_id
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def get_by_id(self, record_id: int):
        return self.db.query(models.Record).filter(models.Record.id == record_id).first()

    def get(self, record_id: int) -> Optional[models.Record]:
        return self.db.query(models.Record).filter(models.Record.id == record_id).first()

    def get_by_content(self, content: str) -> Optional[models.Record]:
        return self.db.query(models.Record).filter(models.Record.content == content).first()

    def update(self, record_id: int, updated_record: schemes.RecordBase) -> Optional[schemes.Record]:
        db_record = self.db.query(models.Record).filter(models.Record.id == record_id).first()
        if db_record:
            for key, value in updated_record.dict().items():
                if value is not None:
                    setattr(db_record, key, value)
            self.db.commit()
            self.db.refresh(db_record)
            return db_record
        return None

    def delete(self, record_id: int) -> bool:
        db_record = self.db.query(models.Record).filter(models.Record.id == record_id).first()
        if db_record:
            self.db.delete(db_record)
            self.db.commit()
            return True
        return False