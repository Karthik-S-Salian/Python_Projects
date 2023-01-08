from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL = "postgresql://<username>:<password>@<ip-address/hostname>"  hostname=database_name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:superuser@localhost/fastapi_tutorial"



engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()