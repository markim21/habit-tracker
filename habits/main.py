from . import models, schemas
from .controllers import list_controller, task_controller
from .database import SessionLocal, engine 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Create database (normally done with Alembic?)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
# TODO: i don't understand this. read https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/ later
def get_db():
    db = SessionLocal() # This is the same connection from database.py.
    try: yield db
    finally: db.close()

"""Create new list."""
@app.post("/lists/", response_model = schemas.List)
def create_list(list: schemas.ListCreate, db: Session = Depends(get_db)):
    return list_controller.create_list(db = db, list = list)

"""Get all lists."""
@app.get("/lists/", response_model = List[schemas.List])
def read_list(db: Session = Depends(get_db)):
    return list_controller.get_all_lists(db)

"""Update list given list_id."""
@app.patch("/lists/{list_id}", response_model = schemas.List)
def update_list(list_id: int, new_data: schemas.List, db: Session = Depends(get_db)):
    return list_controller.update_list(db=db, list_id=list_id, new_data=new_data)

"""Delete list given list_id."""
@app.delete("/lists/{list_id}", response_model = schemas.List)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    return list_controller.delete_list(db=db, list_id=list_id)



"""Create new task given list id."""

"""Get tasks associated with given list id."""

"""Update task description, order in list, completion"""

"""Delete task from given list id."""