import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Retrieve detailed info on the given number '
                                                 'of top selling games on steam in a particular category.')

    parser.add_argument('--config_file_path', type=str, required=True, help='path to configuration file')
    parser.add_argument('--category', type=str, choices=['rpg', 'action', 'strategy', 'adventure', 'simulation', 'sports_racing', 'all'],
                        required=True, help='Game category to scrape. Available options: rpg, action, strategy, adventure, '
                             'simulation, sports_racing')
    parser.add_argument('--num_games', type=int, required=True, help='Number of games to scrape')
    parser.add_argument('--db', type=str, choices=['y', 'n'], required=True,
                        help='Whether to add scraping results to a database. Choose from: y or n.')

    args = parser.parse_args()

    return args
