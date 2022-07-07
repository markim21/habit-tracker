# Create SQL database models and relationships.
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Boolean, Column, Identity, Integer, String, Time
from database import Base

class List(Base):
    __tablename__ = "list"
    id = Column(Integer, primary_key = True)
    title = Column(String, nullable=False)
    description = Column(String)
    reset_time = Column(String)
    notif_time = Column(String)

    tasks = relationship("Task", cascade="all, delete")

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key = True, autoincrement = True)
    list_id = Column(Integer, ForeignKey("list.id", ondelete='CASCADE'))
    title = Column(String, nullable = False)
    description = Column(String)
    order_in_list = Column(Integer, Identity(start=0))
    completed = Column(Boolean)

    #list = relationship("List", back_populates="tasks")