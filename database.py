from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

sqlite_url=os.getenv("DATABASE_URL")

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)






