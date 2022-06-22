# Create SQL database models and relationships.
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Boolean, Column, Integer, String, Time
from .database import Base

class List(Base):
    __tablename__ = "list"
    id = Column(Integer, primary_key = True)
    title = Column(String, nullable=False)
    description = Column(String)
    reset_time = Column(Time)
    notif_time = Column(Time)

    tasks = relationship("Task", back_populates="list")

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key = True, autoincrement = True)
    list_id = Column(Integer, ForeignKey("list.id"))
    title = Column(String, nullable = False)
    description = Column(String)
    order_in_list = Column(Integer)
    completed = Column(Boolean)

    list = relationship("List", back_populates="tasks")