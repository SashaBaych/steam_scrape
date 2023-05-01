import argparse


def parse_args():
    """
    Parses command-line arguments for the Steam scraper script.

    Returns:
        argparse.Namespace: An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Retrieve detailed info on the given number '
                                                 'of top selling games on steam in a particular category.')

    parser.add_argument('--config_file_path', type=str, required=True, help='path to configuration file',
                        default='steam_scrape_conf.json')
    parser.add_argument('--category', type=str,
                        choices=['rpg', 'action', 'strategy', 'adventure', 'simulation', 'sports_racing', 'global'],
                        default='global',
                        help='Game category to scrape. Available options: rpg, action, strategy, adventure, '
                             'simulation, sports_racing. Default: global')
    parser.add_argument('--num_games', type=int, default=10,
                        help='Number of games to scrape. Default: 100')
    parser.add_argument('--db', type=str, choices=['y', 'n'], default='y',
                        help='Whether to add scraping results to a database. Choose from: y or n. Default: y')

    args = parser.parse_args()

    return args

