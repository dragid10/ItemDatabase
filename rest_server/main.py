from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session, create_engine, select

from rest_server.models.items import Items

# SQLModel Docs: https://sqlmodel.tiangolo.com/


### Database Connection ###
sqlite_file_name = "../database.db"
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


@app.get("/items/id/{item_id}")
async def get_item_by_id(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Items, item_id)
    return item


@app.get("/items/barcode/{barcode}")
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
