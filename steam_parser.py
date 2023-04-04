import argparse
import logging
import os


def validate_config_file_path(config_file_path):
    # Check if the file exists and is a file, not a directory.
    if os.path.isfile(config_file_path):
        return config_file_path
    else:
        raise ValueError("Invalid file path. Please provide a valid path to the configuration file.")


def validate_category(category):
    valid_categories = ['rpg', 'action', 'strategy', 'adventure', 'simulation', 'sports_racing']
    if category.lower() in valid_categories:
        return category.lower()
    else:
        raise ValueError(f"Invalid game category. \nPlease choose from: {', '.join(valid_categories)}")


def validate_num_games(num_games):
    if num_games.isdigit() and int(num_games) > 0:
        return int(num_games)
    else:
        raise ValueError("Invalid number of games. Please provide a positive integer value.")


def validate_use_database(use_database):
    if use_database.lower() == 'y' or use_database.lower() == 'n':
        return use_database.lower()
    else:
        raise ValueError("Invalid input. Please enter 'y' or 'n'.")


def parse_args():
    parser = argparse.ArgumentParser(description='Retrieve detailed info on the given number '
                                                 'of top selling games on steam in a particular category.')

    while True:
        try:
            config_file_path = input("Enter the path to the configuration file: ")
            config_file_path = validate_config_file_path(config_file_path)
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            category = input("Enter the game category to scrape. "
                             "\nPlease choose from "
                             "'rpg', 'action', 'strategy', 'adventure', 'simulation', 'sports_racing': ")
            category = validate_category(category)
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            num_games = input("Enter the number of games to scrape: ")
            num_games = validate_num_games(num_games)
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            use_database = input("Do you want to add scraping results to a database? (y/n): ")
            use_database = validate_use_database(use_database)
            break
        except ValueError as e:
            print(e)

    parser.add_argument('--config_file_path', type=str, help='path to configuration file', default=config_file_path)
    parser.add_argument('--category', type=str,
                        choices=['rpg', 'action', 'strategy', 'adventure', 'simulation', 'sports_racing'],
                        help='Game category to scrape. Available options: rpg, action, strategy, adventure, '
                             'simulation, sports_racing', default=category)
    parser.add_argument('--num_games', type=int, help='Number of games to scrape', default=num_games)
    parser.add_argument('--use_database', type=bool, help='Whether to add scraping results to a database',
                        default=True if use_database == 'y' else False)

    args = parser.parse_args()
    return args
