from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:admin123@localhost/uzum_db')

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()