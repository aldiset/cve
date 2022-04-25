from ast import Str
from colorama import Fore
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.engine import Base


class ExecuteFlow(Base):
    __tablename__ = 'execute_flow'
    id = Column(Integer, primary_key=True, autoincrement=True)
    capec_id = Column(Integer)
    step1 = Column(String, nullable=True)
    step2 = Column(String, nullable=True)
    step3 = Column(String, nullable=True)
    step4 = Column(String, nullable=True)
    step5  = Column(String, nullable=True)
    step6 = Column(String, nullable=True)
    step7 = Column(String, nullable=True)
    step8 = Column(String, nullable=True)
    step9 = Column(String, nullable=True)
    step10 = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.now)
    deleted_date = Column(DateTime)

class Capec(Base):
    __tablename__ = 'capec'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    abstraction = Column(String)
    status = Column(String)
    description = Column(String)
    alternate_terms = Column(String)
    likelihood_of_attack = Column(String)
    typical_severity = Column(String)
    related_attack_patterns = Column(String)
    execution_flow = Column(String, ForeignKey("execute_flow.id"))
    prerequisites = Column(String)
    skills_required = Column(String)
    resources_required = Column(String)
    indicators = Column(String)
    consequences = Column(String)
    mitigations = Column(String)
    example_instances = Column(String)
    related_weaknesses = Column(String)
    taxonomy_mappings = Column(String)
    note = Column(String)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, onupdate=datetime.now)
    deleted_date = Column(DateTime)

    executeflow = relationship("ExecuteFlow")
    
