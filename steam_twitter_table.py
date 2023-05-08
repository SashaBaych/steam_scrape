import mysql.connector
from steam_twitter_query import get_mentions_count
from steam_utils import logger_decorator


@logger_decorator
def connect_to_db(db_conf: dict):
    """
    Connects to the MySQL database using the provided configuration.

    Args:
        db_conf (dict): A dictionary containing database connection parameters.

    Returns:
        mysql.connector.connection.MySQLConnection: A connection to the MySQL database.
    """
    return mysql.connector.connect(**db_conf)


@logger_decorator
def get_top_games(db_connection):
    """
    Retrieves the top 10 games with unique game IDs from the MySQL database.

    Args:
        db_connection (mysql.connector.connection.MySQLConnection): A connection to the MySQL database.

    Returns:
        dict: A dictionary containing the top 10 games and their corresponding game_id and rank.
    """
    cursor = db_connection.cursor()
    query = """
    SELECT DISTINCT g.title, tsh.game_id, tsh.position
    FROM top_selling_history tsh
    INNER JOIN game g ON tsh.game_id = g.game_id
    WHERE tsh.sample_date = (
        SELECT MAX(tsh2.sample_date)
        FROM top_selling_history tsh2
        WHERE tsh2.game_id = tsh.game_id
    )
    ORDER BY tsh.position
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    top_games = {}
    for row in rows:
        game_name, game_id, position = row
        top_games[game_name] = {"Id": game_id, "rank": position}

    cursor.close()
    return top_games


@logger_decorator
def create_or_update_twitter_table(db_connection, enriched_games):
    """
    Creates or updates the 'twitter' table in the MySQL database with the enriched games data.

    Args:
        db_connection (mysql.connector.connection.MySQLConnection): A connection to the MySQL database.
        enriched_games (dict): A dictionary containing the enriched games data.
    """
    cursor = db_connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS twitter (
        id INT AUTO_INCREMENT PRIMARY KEY,
        game_id INT,
        mentions_count INT,
        query_date DATE,
        FOREIGN KEY (game_id) REFERENCES game(game_id)
    );
    """
    cursor.execute(create_table_query)

    for game_data in enriched_games.values():
        insert_query = """
        INSERT INTO twitter (game_id, mentions_count, query_date)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        id=id;
        """
        game_id = game_data["Id"]
        mentions_count = game_data["mentions_count"]
        query_date = game_data["query_date"]
        cursor.execute(insert_query, (game_id, mentions_count, query_date))

    db_connection.commit()
    cursor.close()


@logger_decorator
def twitter_enrich(db_conf: dict):
    """
    Connects to the MySQL database, retrieves the top 10 games, enriches the games with Twitter data,
    and updates the 'twitter' table in the MySQL database with the enriched games data.

    Args:
        db_conf (dict): A dictionary containing database connection parameters.
    """
    db_connection = connect_to_db(db_conf)
    top_games = get_top_games(db_connection)
    enriched_games = get_mentions_count(top_games)
    create_or_update_twitter_table(db_connection, enriched_games)
    db_connection.close()
