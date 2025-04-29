from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Boolean, Index, Enum
from sqlalchemy.orm import relationship
from app.Cores.database import Base

class hocsinh(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
