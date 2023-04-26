import json
from steam_parser import parse_args
from steam_sql_tables import deploy_db
from steam_populate_database import populate_database
from steam_create_classes import create_game_catalogue
from steam_utils import get_logger, logger_decorator


logger = get_logger(__file__)

def load_config(config_file_path: str) -> dict:
    """
    Load configuration from the specified JSON file.

    Args:
        config_file_path (str): A string representing the path to the configuration file.

    Returns:
        dict: A dictionary containing the configuration data.

    Raises:
        Exception: If there's an error while loading the configuration from the file.
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
    Runs a simple steam scraper for a given category and number of games
    and adds results to the database on demand.
    """
    args = parse_args()

    config = load_config(args.config_file_path)

    catalogue = create_game_catalogue(config['urls'][args.category], args.num_games, category=args.category)

    if args.db is True:
        deploy_db(config['db_conf'], config['alch_conf']['database'])

        populate_database(catalogue, config['alch_conf'])


if __name__ == '__main__':
    main()











