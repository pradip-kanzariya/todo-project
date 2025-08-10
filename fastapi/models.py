from sqlalchemy import Column, String, Integer, Text
from database import Base

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=200), nullable=False)
    description = Column(Text, nullable=True)

    def __str__(self):
        return self.title
