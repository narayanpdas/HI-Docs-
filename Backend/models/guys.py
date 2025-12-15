from sqlalchemy import Column,String,Integer,ForeignKey
from models.database import Base


class Guys(Base):
    __tablename__ = "guys"
    id = Column(String,primary_key=True)
    api_key = Column(String)
    current_process_doc_id = Column(Integer,ForeignKey("documents.id"),nullable=True, default=None) # doc id underprocess or None if not any.
    def __repr__(self):
        return f"<Guys(id='{self.id}',key='{self.api_key},current_process_doc_id='{self.current_process_doc_id}')>"
