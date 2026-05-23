from app.db.connection import engine, Base

from app.models.client import Client

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("Database tables created!")