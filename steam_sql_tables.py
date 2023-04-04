from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import mysql.connector
from steam_utils import logger_decorator, get_logger

logger = get_logger(__file__)


@logger_decorator
def deploy_db(config_dict, db_name):
    """
    Creates a new MySQL database with the given name if it does not exist, using the provided configuration parameters.

    Parameters:
        config_dict (dict): A dictionary containing the configuration parameters for the MySQL connection.
        The dictionary must contain the keys 'host', 'user', and 'password', and optionally 'port' and 'ssl_mode'.
        db_name (str): The name of the database to be created or checked.

    Raises:
        mysql.connector.Error: If there is an error creating the database or connecting to the MySQL server.
        TypeError: If the configuration dictionary is not provided or is not a dictionary.

    Returns:
        None: This function does not return anything.
    """
    cnx = mysql.connector.connect(**config_dict)
    cursor = cnx.cursor()
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
    cursor.execute(create_database_query)
    cursor.close()
    cnx.close()


Base = declarative_base()

# For more details on the database tables please read the included README.md
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




