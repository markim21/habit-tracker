from . import models, schemas 
from sqlalchemy.orm import Session
from datetime import time

# Create new list.
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

# Get all lists.
def get_all_lists(db: Session):
    return db.query(models.List)

# Update list title, description, reset_time, notif_time/


# Delete list.

