from steam_get_info import get_game_dicts
from steam_scrape_all import get_basic_game_info_all
from steam_scrape_category import get_basic_game_info_category
from steam_game_classes import SteamGameCatalog
from steam_utils import logger_decorator


@logger_decorator
def create_game_catalogue(url: str, num_of_games: int, category: str) -> SteamGameCatalog:

    game_catalogue = SteamGameCatalog(category)

    if category == 'global':
        basic_info = get_basic_game_info_all(url, num_of_games)
    else:
        basic_info = get_basic_game_info_category(url, num_of_games)

    links = [game['link'] for game in basic_info]

    info = get_game_dicts(links)

    for j in range(num_of_games):
        game_catalogue.add_game(rank=basic_info[j]['rank'], name=basic_info[j]['title'],
                                link=basic_info[j]['link'], info=info[j])

    print(game_catalogue)
    return game_catalogue
