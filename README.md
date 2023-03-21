# Sample Steam Scraper

## Why we selected Steam:

We chose Steam as the target for our web scraper for several reasons. Firstly, video games are a medium that I am personally passionate about. However, more importantly, data scientists are increasingly necessary for successful game design. Modern games collect data about every action, move, or click of the player, and a data scientist can use this data to understand the mechanics of a particular game even better than its creators and designers. This can lead not only to better monetization of the game, but also to an overall better player experience. While Steam does not provide this level of data, it still provides valuable insights to marketing and sales specialists and game creators who want to be more successful.

## About the web scraper:

Our web scraper is more of a prototype. It is capable of retrieving the list of top-selling games or a particular genre and enriching it with detailed data from each game's page. This creates a full game profile as a unit in a database. Steam's own stats page shows top-selling games, but it does not allow sorting by genre. However, the scraper can be extended to retrieve top games for every genre and enrich each game's info with as much detail as necessary. This would allow researchers to look for correlations between top-selling games, most-played games, their prices or lack of those if a game is free to play, release date, reviewers’ feedback, etc.

## Major difficulties of the project:

One of the major difficulties of the project was that Steam's pages are dynamic, which required the use of Selenium to "wait" for certain items to fully load on a page and further browser automation. For example, one of the automation features in the pipeline is Selenium automation to bypass the age filter by inputting a birth date to access pages for certain games with age restrictions.


# How it Works

The program is designed to scrape information about the top-selling RPG games on Steam. It retrieves the specified number of games and their details by navigating through Steam's genre webpages and extracting the required information using a combination of `grequests`, `BeautifulSoup`, and `Selenium`.

Here's an overview of the program's functionality:

1. **Command Line Arguments**: The program accepts a single command line argument, the path to a configuration file. This file contains the URL to the Steam genre page and the number of games to retrieve.

2. **Configuration File**: The configuration file is loaded using the `load_config()` function, which returns a dictionary containing the URL and the number of games to retrieve.

3. **Selenium Request**: The `selenium_request()` function is used to retrieve the page source for the Steam genre page. It employs Selenium WebDriver to load the page, wait for the necessary elements to be present, and then retrieve the page's source as a BeautifulSoup object.

4. **Extracting Game Information**: The `get_games()` function extracts the game names, links, and ranks from the BeautifulSoup object. It iterates through the specified number of games, splitting them into groups of 12 (the number of games displayed per loop on the Steam genre page).

5. **GRequests for Game Info**: The `grequests_for_game_info()` function sends asynchronous HTTP requests using `grequests` to fetch the individual game pages for further extraction. It takes a list of game URLs as input and returns a list of response objects.

6. **Getting Game Details**: The `get_info()` function processes the list of response objects returned by `grequests_for_game_info()`. It calls the `get_dict()` function for each response, which extracts game information such as name, release date, price, currency, review summary, and genres.

7. **SteamGame and SteamGameCatalog Classes**: The extracted game information is stored using the `SteamGame` class, which represents an individual game, and the `SteamGameCatalog` class, which is a collection of `SteamGame` objects. The `SteamGameCatalog` class is a subclass of Python's `dict` and provides additional methods for adding, updating, and retrieving game information.

8. **Logging**: Throughout the program, logging statements are used to provide information about the program's progress and any errors that may occur. The log messages are written to a file named `steam_scrape_<timestamp>.log`.

9. **Output**: When the program has finished retrieving the specified number of games, the `SteamGameCatalog` object is printed, displaying the game details in a well-formatted text.
