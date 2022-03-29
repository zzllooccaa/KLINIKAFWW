from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = "postgresql://postgres:myPassword@localhost:5432/Clinic22"
#DATABASE_URL = "postgresql://postgres:myPassword@localhost:5430/Clinic22" #docker port

engine = create_engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

path_images = os.path.join(os.path.dirname(__file__), "static/images")
path_doc = os.path.join(os.path.dirname(__file__), "static/document")
path_req = os.path.join(os.path.dirname(__file__), "static/requirements")
path_temp = os.path.join(os.path.dirname(__file__), "temp_files")
