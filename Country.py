from sqlalchemy import Column, Integer, Text
from db_config import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(Text(), unique=True, nullable=False)

    def __eq__(self, other):
        if not isinstance(other, Country):
            return False
        else:
            return self.id == other.id and self.name == other.name
    def __str__(self):
        return f'Country[id={self.id}, name={self.name}]'

    def __repr__(self):
        return f'Country(id={self.id}, name={self.name})'

