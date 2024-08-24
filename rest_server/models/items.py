from datetime import date
from typing import List

from sqlmodel import Field, Relationship, SQLModel


class Items(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    barcode: str = Field(max_length=255, unique=True, index=True)
    description: str | None = Field(max_length=500, default=None)
    quantity: int = Field(default=1)
    type: str = Field(max_length=50)
    purchase_date: date | None = Field(default=None)
    warranty_link: str | None = Field(default=None, max_length=255)
    loans: List["Loans"] = Relationship(back_populates="item")
