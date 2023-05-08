import json
from steam_parser import parse_args
from steam_sql_tables import deploy_db
from steam_populate_database import populate_database
from steam_create_classes import create_game_catalogue
from steam_twitter_table import twitter_enrich
from steam_utils import get_logger, logger_decorator


logger = get_logger(__file__)


def load_config(config_file_path: str) -> dict:
    """
    Loads configuration data from a JSON file.

    Parameters:
    file_path (str): The path to the JSON file containing the configuration data.

    Returns:
    dict: A dictionary containing the configuration data.
    """
    try:
        logger.info(f"Loading configuration from {config_file_path}...")
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Error while loading configuration: {e}")
        logger.info("Terminating program gracefully.")
        exit()


@logger_decorator
def main():
    """
    The main function to run the Steam web scraper and populate the database.

    This function reads the configuration file, runs the web scraper to collect
    information about the top-selling games on Steam, creates a catalog object,
    and populates the MySQL database with the scraped data. Enriches database
    with data from twitter if requested by user.
    """
    args = parse_args()

    config = load_config(args.config_file_path)

    catalogue = create_game_catalogue(config['urls'][args.category], args.num_games, category=args.category)

    if args.db == 'y':
        deploy_db(config['db_conf'], config['alch_conf']['database'])

        populate_database(catalogue, config['alch_conf'])
    if args.tw == 'y':
        twitter_enrich(config['db_conf'])


if __name__ == '__main__':
    main()







