from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    google_drive_refresh_token = Column(String, nullable=True)
    google_drive_folder_id = Column(String, nullable=True)
    shortio_domain = Column(String, nullable=True)
    shortio_api_key = Column(String, nullable=True)

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, is_admin={self.is_admin})>"

