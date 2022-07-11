from http.client import HTTPException
import json
import models
import schemas 
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

def get_list(db: Session, list_id: int):
    list = db.query(models.List).filter(models.List.id==list_id).first()
    if list is None:
        raise HTTPException(status_code=404, detail="List not found")

    return list


# Create new task, given list id.
def add_task(task: schemas.TaskCreate, db: Session):
    list_id = task.list_id
    title = task.title

    list = get_list(db=db, list_id=list_id)

    tasks = jsonable_encoder( list.tasks )

    order = 0
    if len(tasks) > 0:
        order = len(tasks)

    new_task = models.Task(
        list_id = list_id,
        title = title,
        completed = False,
        description = task.description,
        order_in_list = order
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return jsonable_encoder(new_task)
        

# Get all tasks associated with given list id.
def get_list_tasks(db: Session, list_id: int):
    get_list(db, list_id)
    tasks = db.query(models.Task).filter(models.Task.list_id == list_id).all()
    return tasks
    

# Update task description, order in list, completion.
def update_task(db: Session, new_data = schemas.Task):
    id = new_data.id

    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None: 
        raise HTTPException(status_code=404, detail="Task not found.")

    current_task_model = schemas.Task(**jsonable_encoder(task))

    updated_data = new_data.dict(exclude_unset = True)

    updated_task = current_task_model.copy(update=updated_data)

    db.query(models.Task).filter(models.Task.id == id).update(jsonable_encoder(updated_task))

    db.commit()

    return updated_task


# Delete task from list. 
def delete_task(db: Session, id: int):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None:
        raise HTTPException(status_code = 404, detail="Task not found.")

    task_json = jsonable_encoder(task)

    db.delete(task)
    db.commit()

    return task_json 
