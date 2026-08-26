from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# SQLite database file project folder ke andar khud ban jayegi
SQLALCHEMY_DATABASE_URL = "sqlite:///./cyberforges.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 1. Scans Table
class ScanRecord(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, index=True)
    total_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# 2. Leads Table
class LeadRecord(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    company = Column(String, nullable=True)
    email = Column(String)
    phone = Column(String)
    domain = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)