from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List


class RecordBase(BaseModel):
    date: date
    title: str
    content: str


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int
    user_id: int

    class ConfigDict:
        from_attributes = True


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    records: List[Record]

    class ConfigDict:
        from_attributes = True
