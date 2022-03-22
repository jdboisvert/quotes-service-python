from sqlalchemy import Column, Integer, String, UniqueConstraint

from database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    quote = Column(String, unique=True)
    author_name = Column(String)

    __table_args__ = (
        UniqueConstraint("quote", "author_name", name="unique_quote_author_name"),
    )
