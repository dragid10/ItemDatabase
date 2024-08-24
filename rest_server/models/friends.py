from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Friends(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    phone_number: str = Field(max_length=20, index=True)
    email: str | None = Field(default=None, max_length=255)
    loans: List["Loans"] = Relationship(back_populates="friend")
