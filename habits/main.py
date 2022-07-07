#from . import models, schemas
import models, schemas
import list_controller, task_controller
from database import SessionLocal, engine
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
@app.post("/lists", response_model = schemas.List)
def create_list(list: schemas.ListCreate, db: Session = Depends(get_db)):
    return list_controller.create_list(db = db, list = list)


"""Get all lists."""
@app.get("/lists", response_model = List[schemas.List])
def read_list(db: Session = Depends(get_db)):
    return list_controller.get_all_lists(db=db)
  

"""Update list given list_id."""
@app.patch("/lists/{list_id}", response_model = schemas.List)
def update_list(list_id: int, new_data: schemas.List, db: Session = Depends(get_db)):
    return list_controller.update_list(db=db, list_id=list_id, new_data=new_data)


"""Delete list given list_id."""
@app.delete("/lists/{list_id}", response_model = schemas.List)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    return list_controller.delete_list(db=db, list_id=list_id)



"""Create new task given list id."""
@app.post("/lists/{list_id}", response_model = schemas.Task)
def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_controller.add_task(task=task, db=db)


"""Get tasks associated with given list id."""
@app.get("/lists/{list_id}", response_model = List[schemas.Task])
def get_task(list_id: int, db: Session = Depends(get_db)):
    return task_controller.get_list_tasks(db=db, list_id=list_id)


"""Update task description, order in list, or completion"""
@app.patch("/lists/tasks/{id}", response_model = schemas.Task)
def update_task(new_data: schemas.Task, db: Session = Depends(get_db)):
    return task_controller.update_task(db=db, new_data=new_data)


"""Delete task from given list id."""
@app.delete("/lists/tasks/{id}", response_model = schemas.Task)
def delete_task(id: int, db: Session = Depends(get_db)):
    return task_controller.delete_task(db=db, id=id)


"""Debug: Delete all lists."""
@app.delete("/drop")
def drop_all_lists(db: Session = Depends(get_db)):
    db.query(models.List).delete()
    db.query(models.Task).delete()
    db.commit()

    return {"All lists dropped.": True}

 
##if __name__ == "__main__":
##    app.run(host="0.0.0.0", port=4500, debug=True)