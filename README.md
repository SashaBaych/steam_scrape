# Sample Steam Scraper

## Why we selected Steam:

We chose Steam as the target for our web scraper for several reasons. Firstly, video games are becoming a more inspiring anc comprlling medium every high pace. However, more importantly, data scientists are increasingly necessary for successful game design. Modern games collect data about every action, move, or click of the player, and a data scientist can use this data to understand the mechanics of a particular game even better than its creators and designers. This can lead not only to better monetization of the game, but also to an overall better player experience. While Steam does not provide this level of data, it still provides valuable insights to marketing and sales specialists and game creators who want to be more successful.

## About SteamScraper scraper:

This scraper retrieves the list of top-selling games or a particular category from Steam and enriches it with detailed data from each game's page. The data is stored in a MySQL database.  

More detail may be added if necessary. This would allow researchers to look for correlations between top-selling games, most-played games, their prices or lack of those if a game is free to play, release date, reviewers’ feedback, etc.

## Major difficulties of the project:

One of the major difficulties of the project was that Steam's pages are dynamic, which required the use of Selenium to "wait" for certain items to fully load on a page and further browser automation. For example some games are hidden behind age and gegraphic restrictions which needed to be bypassed using selenium.


## How it Works

The Steam scraper program consists of several Python scripts that work together to retrieve and store data on the top-selling games on Steam, as well as their details. Here's how it works:

1. The `steam_main.py` script retrieves the list of top-selling games in each category from the Steam website, using the URLs to pages of categories provided in the `steam_scrape_conf.json` configuration file.
****Note: The user must manually input the required parameters for MySQL access in the configuration file.**
2. It then retrieves the details for each game by visiting their individual game pages using Selenium and Beautiful Soup libraries. The `steam_age_bypass.py` script helps bypass Steam's age verification check, which would otherwise prevent the scraper from accessing the game pages.

3. The data on each game is stored as a `Game` object in memory, which is then added to a catalog of all the games retrieved during the scraping process.

4. The `steam_parser.py` script retrieves user input on the number of games to scrape, the category to scrape, and whether to use a database to store the scraped data. It also validates the user input.

5. If the user chooses to use a database, the `steam_sql_tables.py` script deploys the MySQL database and defines the schema using SQLAlchemy. It also defines helper functions to populate the database with the scraped data.

6. Finally, the `steam_populate_database.py` script populates the database with the scraped data using the helper functions defined in the `steam_sql_tables.py` script.
