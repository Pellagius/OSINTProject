from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Query(Base):
    __tablename__ = 'queries'

    id = Column(Integer, primary_key=True, index=True)
    parameters = Column(JSON, nullable=True)
    created_at = Column(DateTime)

    reports = relationship("Report", back_populates="query")

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # e.g., "Person", "Organization"
    extraData = Column(JSON, nullable=True)  # For any extra details about the subject

    reports = relationship("Report", back_populates="subject")

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey('queries.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    raw_data = Column(Text, nullable=True)  # The messy data from scrapers
    analyzed_content = Column(Text, nullable=True)  # The LLM's refined output
    timestamp = Column(DateTime)

    subject = relationship("Subject", back_populates="reports")
    query = relationship("Query", back_populates="reports")
