from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker



Base = declarative_base()


class Developer(Base):
    __tablename__ = 'developer'
    developer_id = Column(Integer, primary_key=True)
    name = Column(String(255))

class Publisher(Base):
    __tablename__ = 'publisher'
    publisher_id = Column(Integer, primary_key=True)
    name = Column(String(255))


class ReviewSummary(Base):
    __tablename__ = 'review_summary'
    review_summary_id = Column(Integer, primary_key=True)
    summary = Column(String(255))


class Genre(Base):
    __tablename__ = 'genre'
    genre_id = Column(Integer, primary_key=True)
    name = Column(String(255))


game_genre = Table('game_genre', Base.metadata,
    Column('game_id', Integer, ForeignKey('game.game_id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genre.genre_id'), primary_key=True))


class Game(Base):
    __tablename__ = 'game'
    game_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    category = Column(String(255))
    release_date = Column(Date)
    metacritic_score = Column(Integer)
    developer_id = Column(Integer, ForeignKey('developer.developer_id'))
    publisher_id = Column(Integer, ForeignKey('publisher.publisher_id'))
    review_summary_id = Column(Integer, ForeignKey('review_summary.review_summary_id'))

    developer = relationship('Developer')
    publisher = relationship('Publisher')
    review_summary = relationship('ReviewSummary')
    genres = relationship('Genre', secondary=game_genre, backref='games')


class PriceHistory(Base):
    __tablename__ = 'price_history'
    price_history_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id'))
    price = Column(Float)
    currency = Column(String(255))
    sample_date = Column(Date)

    game = relationship('Game')


class TopSellingHistory(Base):
    __tablename__ = 'top_selling_history'
    top_selling_history_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id'))
    position = Column(Integer)
    sample_date = Column(Date)

    game = relationship('Game')




