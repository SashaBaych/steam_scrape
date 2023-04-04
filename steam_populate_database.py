# from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float, Table
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from steam_sql_tables import *
from steam_utils import get_logger, logger_decorator

@logger_decorator
def populate_developer(session, developer_name):
    developer = session.query(Developer).filter_by(name=developer_name).first()
    if not developer:
        developer = Developer(name=developer_name)
        session.add(developer)
        session.commit()
    return developer

@logger_decorator
def populate_publisher(session, publisher_name):
    publisher = session.query(Publisher).filter_by(name=publisher_name).first()
    if not publisher:
        publisher = Publisher(name=publisher_name)
        session.add(publisher)
        session.commit()
    return publisher

@logger_decorator
def populate_review_summary(session, review_summary_desc):
    review_summary = session.query(ReviewSummary).filter_by(summary=review_summary_desc).first()
    if not review_summary:
        review_summary = ReviewSummary(summary=review_summary_desc)
        session.add(review_summary)
        session.commit()
    return review_summary

@logger_decorator
def populate_genre(session, genre_name):
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()
    return genre

@logger_decorator
def populate_game(session, game):
    developer = populate_developer(session, game.info['developer'])
    publisher = populate_publisher(session, game.info['publisher'])
    review_summary = populate_review_summary(session, game.info['review_summary'])
    genres = [populate_genre(session, genre_name) for genre_name in game.info['genres']]

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

    return game_entry

@logger_decorator
def populate_price_history(session, game_entry, price, currency, rank_date):
    price_history = PriceHistory(
        game_id=game_entry.game_id,
        price=price,
        currency=currency,
        sample_date=rank_date
    )
    session.add(price_history)
    session.commit()

@logger_decorator
def populate_top_selling_history(session, game_entry, rank, rank_date):
    top_selling_history = TopSellingHistory(
        game_id=game_entry.game_id,
        position=rank,
        sample_date=rank_date
    )
    session.add(top_selling_history)
    session.commit()

@logger_decorator
def populate_database(catalog: object, db_config: dict):
    db_url = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    for game_name, game in catalog.items():
        game_entry = populate_game(session, game)
        populate_price_history(session, game_entry, game.info['price'],
                               game.info['price_currency'], game.info['sample_date'])
        populate_top_selling_history(session, game_entry, game.rank, game.info['sample_date'])
        session.commit()
    print('It actually worked')
    session.close()
