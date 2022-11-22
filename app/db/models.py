from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, String


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    first_name = Column(String)

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
