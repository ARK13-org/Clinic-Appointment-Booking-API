from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///Booking.db", connect_args={"check_same_thread": False})
base = declarative_base()
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()