from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./researchhub.db"

engine = create_engine(DATABASE_URL)