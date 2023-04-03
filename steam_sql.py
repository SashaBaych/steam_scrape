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


def populate_database(catalog):
    engine = create_engine('sqlite:///steamgames.db', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for game_name, game in catalog.items():
        # Insert or update the developer, publisher, review_summary, and genres
        developer = session.query(Developer).filter_by(name=game.info['developer']).first()
        if not developer:
            developer = Developer(name=game.info['developer'])
            session.add(developer)
            session.commit()

        publisher = session.query(Publisher).filter_by(name=game.info['publisher'])
        publisher = session.query(Publisher).filter_by(name=game.info['publisher']).first()
        if not publisher:
            publisher = Publisher(name=game.info['publisher'])
            session.add(publisher)
            session.commit()

        review_summary = session.query(ReviewSummary).filter_by(summary=game.info['review_summary']).first()
        if not review_summary:
            review_summary = ReviewSummary(summary=game.info['review_summary'])
            session.add(review_summary)
            session.commit()

        genres = []
        for genre_name in game.info['genres']:
            genre = session.query(Genre).filter_by(name=genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
                session.add(genre)
                session.commit()
            genres.append(genre)

        # Insert or update the game
        game_entry = session.query(Game).filter_by(title=game.name).first()
        if not game_entry:
            game_entry = Game(
                title=game.name,
                category=game.category,
                release_date=game.info['release_date'],
                metacritic_score=game.info['metacritic_score'],
                developer_id=developer.developer_id,
                publisher_id=publisher.publisher_id,
                review_summary_id=review_summary.review_summary_id,
                genres=genres
            )
            session.add(game_entry)
            session.commit()
        else:
            game_entry.category = game.category
            game_entry.release_date = game.info['release_date']
            game_entry.metacritic_score = game.info['metacritic_score']
            game_entry.developer_id = developer.developer_id
            game_entry.publisher_id = publisher.publisher_id
            game_entry.review_summary_id = review_summary.review_summary_id
            game_entry.genres = genres
            session.commit()

        # Insert the price history
        price_history = PriceHistory(
            game_id=game_entry.game_id,
            price=game.info['price'],
            currency=game.info['price_currency'],
            sample_date=game.rank_date  # Assuming you have rank_date attribute in SteamGame class
        )
        session.add(price_history)
        session.commit()

        # Insert the top selling history
        top_selling_history = TopSellingHistory(
            game_id=game_entry.game_id,
            position=game.rank,
            sample_date=game.rank_date  # Assuming you have rank_date attribute in SteamGame class
        )
        session.add(top_selling_history)
        session.commit()

    session.close()



