from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    skills = Column(String, index=True)
    experience = Column(String, index=True)
    education = Column(String, index=True)

class Vacancy(Base):
    __tablename__ = 'vacancies'  # Имя таблицы в базе данных

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(String, index=True)
    location = Column(String, index=True)