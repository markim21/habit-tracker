from http.client import HTTPException
import models 
import schemas

from sqlalchemy.orm import Session
from datetime import time
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

"""Create new list."""
def create_list(db: Session, list: schemas.ListCreate):
    new_list = models.List(
        title = list.title,
        description = list.description,
        reset_time = list.reset_time,
        notif_time = list.notif_time
    )

    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list

"""Get all lists."""
def get_all_lists(db: Session):
    return db.query(models.List).all()

""" Update list title, reset_time, notif_time """
def update_list(db: Session, list_id: int, new_data: schemas.List):
    # Retrieve stored data.
    list = db.query(models.List).filter(models.List.id == list_id).first()
    if list is None:
        raise HTTPException(status_code = 404, detail="List not found.") # DOES THIS SHOW UP IN REDOC????

    # Put stored data in model
    current_list_model = schemas.List(**jsonable_encoder(list))

    # Generate dict without default values from the input model
    updated_data = new_data.dict(exclude_unset = True)

    # create copy of stored model and update it with new data. 
    updated_list = current_list_model.copy(update=updated_data)

    final_list = jsonable_encoder(updated_list)
    final_list.pop('tasks')

    # convert stored model copy into something DB can store
    db.query(models.List).filter(models.List.id==list_id).update(final_list)

    # save data to DB 
    db.commit()

    # return updated model
    return updated_list


"""Delete list."""
def delete_list(db: Session, list_id: int):
    list = db.query(models.List).filter(models.List.id==list_id).first()

    if list is None:
        raise HTTPException(status_code = 404, detail="List not found.")

    db.delete(list)
    db.commit()

    return list_json

