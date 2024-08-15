from sqlalchemy import Column, Integer, String
from .database import Base


class UserData(Base):
    __tablename__ = 'user_data'

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<phone_number={self.phone_number}>"
