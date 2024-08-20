from contextlib import asynccontextmanager
from datetime import date
from typing import List

from fastapi import Depends, FastAPI
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, select


# SQLModel Docs: https://sqlmodel.tiangolo.com/


### Start Models ###


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


class Friends(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    phone_number: str = Field(max_length=20, index=True)
    email: str | None = Field(default=None, max_length=255)
    loans: List["Loans"] = Relationship(back_populates="friend")


class Loans(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    friend_id: int = Field(foreign_key="friends.id", index=True)
    borrow_date: date
    return_date: date | None = Field(default=None, index=True)
    item: Items = Relationship(back_populates="loans")
    friend: Friends = Relationship(back_populates="loans")


### End Models ###

### Database Connection ###
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


### End Database Connection ###

### LifeSpan Events ###
def create_db_and_tables() -> None:
    """ Initialize database and tables """
    SQLModel.metadata.create_all(engine)
    print("Database and tables created")


def close_db_connection():
    """ Close database connection """
    engine.dispose()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    close_db_connection()


### End LifeSpan Events ###

app: FastAPI = FastAPI(lifespan=lifespan)


### Dependency Injection ###
def get_session():
    with Session(engine) as session:
        yield session


### End Dependency Injection ###


### Routes ###
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/items")
async def get_all_items(session: Session = Depends(get_session)):
    items = session.query(Items).all()
    return items


@app.get("/items/{item_id}")
async def get_item_by_id(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Items, item_id)
    return item


@app.get("/items/{barcode}")
async def get_item_by_barcode(barcode: str, session: Session = Depends(get_session)):
    item = session.exec(select(Items).where(Items.barcode == barcode)).first()
    return item


# Get all loaned items
@app.get("/items/loaned")
async def get_all_loaned_items(session: Session = Depends(get_session)):
    items = session.exec(select(Items).where(Items.loans is not None)).all()
    return items


# Get all loaned items by type
@app.get("/items/loaned/{type}")
async def get_all_loaned_items_by_type(item_type: str, session: Session = Depends(get_session)):
    items = session.exec(select(Items).where(Items.loans is not None, Items.type == item_type)).all()


# Get all loaned items by friend
@app.get("/items/loaned/{friend_id}")
async def get_all_loaned_items_by_friend(friend_id: int, session: Session = Depends(get_session)):
    items = session.exec(select(Items).where(Items.loans is not None, Items.loans.friend_id == friend_id)).all()
    return items


@app.post("/items")
async def add_item(item: Items, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
### End Routes ###
