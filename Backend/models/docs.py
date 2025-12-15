from sqlalchemy import Column,Integer,String,ForeignKey,Boolean
# from models.user import Base
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from models.database import Base

# Base = declarative_base()


class Documents(Base):
    __tablename__ = "documents"
    id = Column(Integer,primary_key=True)
    
    name = Column(String,nullable=False)
    path = Column(String,nullable=False,unique=True)
    hash = Column(String,unique=True)
    is_processed = Column(Boolean,nullable=False,default=False)
    user_links = relationship('UserDocuments',back_populates='document')
    def __repr__(self):
        return f"<Documents(id='{self.id}',name='{self.name},path='{self.path}',is_processes='{self.is_processed}')>"
    
    
class UserDocuments(Base):
    __tablename__ = "user_documents"
    id=Column(Integer,primary_key=True,index=True)
    
    user_id = Column(String,ForeignKey('guys.id'))
    file_id = Column(String,ForeignKey('documents.id'))
    filename = Column(String,nullable=True)
    
    document = relationship('Documents',back_populates='user_links')
    def __repr__(self):
        return f"<UserDocuments(id='{self.id}',name='{self.filename}',owner='{self.user_id}',file_hash='{self.file_id}')>"