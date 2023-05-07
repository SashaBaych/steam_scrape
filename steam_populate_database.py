from sqlalchemy.orm import sessionmaker
from steam_sql_tables import *
from steam_utils import get_logger, logger_decorator

logger = get_logger(__file__)

# See below the list of tables that populate corresponding tables in the database.


@logger_decorator
def populate_developer(session, developer_name):
    """
    Populates the Developer table in the database with the given developer name.

    Args:
        session (Session): A SQLAlchemy session object.
        developer_name (str): The name of the developer.

    Returns:
        Developer: A Developer object representing the populated database entry.
    """
    developer = session.query(Developer).filter_by(name=developer_name).first()
    if not developer:
        developer = Developer(name=developer_name)
        session.add(developer)
        session.commit()
    return developer


@logger_decorator
def populate_publisher(session, publisher_name):
    """
    Populates the Publisher table in the database with the given publisher name.

    Args:
        session (Session): A SQLAlchemy session object.
        publisher_name (str): The name of the publisher.

    Returns:
        Publisher: A Publisher object representing the populated database entry.
    """
    publisher = session.query(Publisher).filter_by(name=publisher_name).first()
    if not publisher:
        publisher = Publisher(name=publisher_name)
        session.add(publisher)
        session.commit()
    return publisher


@logger_decorator
def populate_review_summary(session, review_summary_desc):
    """
    Populates the ReviewSummary table in the database with the given review summary description.

    Args:
        session (Session): A SQLAlchemy session object.
        review_summary_desc (str): The description of the review summary.

    Returns:
        ReviewSummary: A ReviewSummary object representing the populated database entry.
    """
    review_summary = session.query(ReviewSummary).filter_by(summary=review_summary_desc).first()
    if not review_summary:
        review_summary = ReviewSummary(summary=review_summary_desc)
        session.add(review_summary)
        session.commit()
    return review_summary


@logger_decorator
def populate_genre(session, genre_name):
    """
    Populates the Genre table in the database with the given genre name.

    Args:
        session (Session): A SQLAlchemy session object.
        genre_name (str): The name of the genre.

    Returns:
        Genre: A Genre object representing the populated database entry.
    """
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()
    return genre


@logger_decorator
def populate_game(session, game):
    """
    Populates the Game table in the database with the given game object.

    Args:
        session (Session): A SQLAlchemy session object.
        game (SteamGame): A SteamGame object containing game information.

    Returns:
        Game: A Game object representing the populated database entry.
    """
    logger.info(f"Populating the 'game' table in the database for {game.name}")
    developer = populate_developer(session, game.info['developer'])
    publisher = populate_publisher(session, game.info['publisher'])
    review_summary = populate_review_summary(session, game.info['review_summary'])
    genres = [populate_genre(session, genre_name) for genre_name in game.info['genres']] if game.info['genres'] else []


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
        )
        if genres:
            game_entry.genres = genres
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
    """
    Populates the PriceHistory table in the database with the given game entry, price, currency, and date.

    Args:
        session (Session): A SQLAlchemy session object.
        game_entry (Game): A Game object representing a database entry.
        price (float): The price of the game.
        currency (str): The currency of the price.
        rank_date (datetime.date): The date when the price was sampled.

    """
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
    """
    Populates the TopSellingHistory table in the database with the given game entry, rank, and date.

    Args:
        session (Session): A SQLAlchemy session object.
        game_entry (Game): A Game object representing a database entry.
        rank (int): The game's rank in the top-selling list.
        rank_date (datetime.date): The date when the rank was sampled.
    """
    top_selling_history = TopSellingHistory(
        game_id=game_entry.game_id,
        position=rank,
        sample_date=rank_date
    )
    session.add(top_selling_history)
    session.commit()

@logger_decorator
def populate_database(catalog: object, db_config: dict):
    """
    Populates the database with the game catalog and the database configuration.

    Args:
        catalog (SteamGameCatalog): A SteamGameCatalog object containing the game catalog.
        db_config (dict): A dictionary containing the database configuration parameters.
    """
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
