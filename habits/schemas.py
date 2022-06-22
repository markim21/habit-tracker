# Define pydantic models (schemas) 
# Used when reading data (ie, returing data from the API,
# so we know what type it is)

# We create a Base model and Creation model 

from typing import Optional, List
from datetime import time
from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    order_in_list: int
    completed: bool

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    list_id: int
    class Config: 
        orm_mode = True


# These base models make sure all list-related models 
# have the same common attributes when creating or reading data.
class ListBase(BaseModel):
    title: str
    description: Optional[str]
    reset_time: time
    notif_time: time

class ListCreate(ListBase):
    pass

# These Models are what's used when reading data/returning from the API
class List(ListBase):
    id: int
    tasks: List[Task] = []
    class Config: 
        # tell pydantic model to read data whether its a dict or ORM model. 
        # ie, if data["column"] isn't right, try data.column.
        orm_mode = True

