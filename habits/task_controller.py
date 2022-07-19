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
        

# Get all tasks associated with given list id, ordered by order_in_list
def get_list_tasks(db: Session, list_id: int):
    get_list(db, list_id)
    tasks = db.query(models.Task).filter(models.Task.list_id == list_id).order_by(models.Task.order_in_list.asc()).all()
    return tasks
    

""" 
Shift the order of all the tasks above/below the changed task.
old_p: where the task was originally
new_p: the new order placement of the task
"""
def update_order(db: Session, new_data: schemas.Task):
    # Get new task order + task itself
    id = new_data.id
    new_p = new_data.order_in_list

    # Get current task order 
    task_to_move = db.query(models.Task).filter(models.Task.id == id).first()
    if task_to_move is None: 
        return HTTPException(status_code = 404)
    old_p = task_to_move.order_in_list

    # Do we push nodes up or down? 
    push_down = False
    if old_p > new_p: push_down = True

    # Starting index
    i = old_p + 1
    if push_down: i = old_p - 1

    # End index
    end = new_p + 1
    if push_down: end = new_p - 1

    # Push all tasks up or down
    while i != end:
        task = db.query(models.Task).filter(models.Task.order_in_list == i).first()

        # if pushing UP, new_order -- 
        # if pushing DOWN, new_order ++ 
        new_order = task.order_in_list - 1 
        if push_down: new_order = task.order_in_list + 1

        json = {"id": task.id,"order_in_list": new_order} 
        jason = schemas.Task(**json)  

        update_task(db=db, new_data=jason) 

        if push_down:
            i -= 1
        else:
            i += 1
    # end loop

    json = {"id": id, "order_in_list": new_p}
    jason = schemas.Task(**json)
    return update_task(db=db, new_data=jason)


# Update task description, order in list, completion.
def update_task(db: Session, new_data = schemas.Task):
    id = new_data.id

    # Get current task information
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None: 
        raise HTTPException(status_code=404, detail="Task not found.")

    # Make schema from current task
    current_task_model = schemas.Task(**jsonable_encoder(task))

    # Put new data into dictionary
    updated_data = new_data.dict(exclude_unset = True)

    # Update schema with new data
    updated_task = current_task_model.copy(update=updated_data)

    # Update database with schema
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
