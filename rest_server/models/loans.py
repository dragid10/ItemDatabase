from datetime import date

from sqlmodel import Field, Relationship, SQLModel

from rest_server.models.items import Items
from rest_server.models.friends import Friends


class Loans(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    friend_id: int = Field(foreign_key="friends.id", index=True)
    borrow_date: date
    return_date: date | None = Field(default=None, index=True)
    item: Items = Relationship(back_populates="loans")
    friend: Friends = Relationship(back_populates="loans")
