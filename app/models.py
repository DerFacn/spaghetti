from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    uuid: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
