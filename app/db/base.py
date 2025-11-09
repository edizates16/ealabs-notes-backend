# app/db/base.py

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Tüm SQLAlchemy modelleri için temel sınıf.
    """
    pass