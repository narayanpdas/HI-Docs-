from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from models.database import Base



class ChatHistory(Base):
    __tablename__= "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    response = Column(JSON)
    owner_id = Column(Integer , ForeignKey("users.id"))
    owner = relationship("User",back_populates="chats")
    

