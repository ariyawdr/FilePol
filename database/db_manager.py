from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User
from ..config.settings import settings

class DBManager:
    def __init__(self, database_url: str = settings.DATABASE_URL):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def get_or_create_user(self, telegram_id: int) -> User:
        session = self.get_session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if not user:
            user = User(telegram_id=telegram_id)
            session.add(user)
            session.commit()
            session.refresh(user)
        session.close()
        return user

    def update_user(self, user: User):
        session = self.get_session()
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        session = self.get_session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        session.close()
        return user

# Initialize DBManager globally or as needed
db_manager = DBManager()

