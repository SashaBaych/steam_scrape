# Sample Steam Scraper

## Why we selected Steam:

We chose Steam as the target for our web scraper for several reasons. Firstly, video games are becoming a more 
inspiring and compelling medium every high pace. However, more importantly, 
data scientists are increasingly necessary for successful game design. 
Modern games collect data about every action, move, or click of the player, 
and a data scientist can use this data to understand the mechanics of a particular game 
even better than its creators and designers. This can lead not only to better monetization of the game, 
but also to an overall better player experience. While Steam does not provide this level of data, 
it still provides valuable insights to marketing and sales specialists and game creators who want to be more successful.

## About SteamScraper scraper:

This scraper retrieves the list of top-selling games or a particular category from Steam and enriches it with detailed data from each game's page. The data is stored in a MySQL database.  

More detail may be added if necessary. This would allow researchers to look for correlations between top-selling games, most-played games, their prices or lack of those if a game is free to play, release date, reviewers’ feedback, etc.

## Major difficulties of the project:

One of the major difficulties of the project was that Steam's pages are dynamic, which required the use of Selenium to "wait" for certain items to fully load on a page and further browser automation. For example some games are hidden behind age and geographic restrictions which needed to be bypassed using selenium. This noticeably slows the scraper down.


## How it Works

The Steam scraper program consists of several Python scripts that work together to retrieve and store data on the top-selling games on Steam, as well as their details. Here's how it works:

1. Run the steam_main.py script to start the scraper. The script will prompt you to input the required scraping parameters (number of games to scrape, category to scrape, and whether to store the scraped data in a database).

   _Note: The user must manually input the required parameters for MySQL access in the steam_scrape_conf.json configuration file._

2. The script retrieves the list of top-selling games in each category from the Steam website, using the URLs to pages of categories provided in the steam_scrape_conf.json configuration file.

3. It then retrieves the details for each game by visiting their individual game pages using Selenium and Beautiful Soup libraries. The steam_age_bypass.py script helps bypass Steam's age verification check, which would otherwise prevent the scraper from accessing the game pages.

4. The data on each game is stored as a Game object in memory, which is then added to a catalog of all the games retrieved during the scraping process.

5. If the user chooses to use a database, the steam_sql_tables.py script deploys the MySQL database and defines the schema using SQLAlchemy. It also defines helper functions to populate the database with the scraped data.

6. Finally, the steam_populate_database.py script populates the database with the scraped data using the helper functions defined in the steam_sql_tables.py script.

7. In addition, the user is given and option to enrich the database with information from twitter
   using Twitter API. In particular, retrieve today's number of Twitter mentions for top 10 games 
   according to the latest scraping date.In addition, the user is given and option to enrich the database with information from twitter
   using Twitter API. In particular, retrieve today's number of Twitter mentions for top 10 games 
   according to the latest scraping date. 


## How to Run the Script

1. Edit the steam_scrape_conf.json configuration file with your MySQL access parameters.
2. Run the steam_main.py script with the path to the configuration file as a mandatory argument:

   `python steam_main.py --config_path path/to/steam_scrape_conf.json`

3. Available parser arguments and options:
   - `config_path`: Path to the configuration file (mandatory).
   - `category`: Name of the category of games to scrape that points to corresponding link (default `general`: top-selling games URL).
   - `num_of_games`: Number of games to scrape (default: 100).
   - `db`: Set this flag to `y` or `n` store the scraped data in a database (default: `y`).
   - `tw`: Set this flag to `y` or `n` enrich database with data from twitter (default: `n`).

4. If needed, adjust the required scraping parameters (number of games to scrape, category to scrape,  
   and whether to store the scraped data in a database and enrich data with information from Twitter). 

## Recommended application

The best case application is to run scraper every set period of rime to track price changes 
for a game in a particular category. 
This will allow to build a comprehensive track of price changes and rating changes for a game.
The specific drawback of this scraper is that it does not take into account the fact that a game 
can belong to multiple categories at the same time so every time the scraper encounters such game, 
its record in the database is rewritten with new category and different top-selling position from a new category,
which mixes up observations.

## Database Schema

The database schema consists of the following tables:

1. **game**: This table stores information about individual games.
   - `game_id`: Primary key, an integer uniquely identifying the game.
   - `title`: The name of the game.
   - `category`: The category of the game (e.g., Action, Adventure, etc.).
   - `release_date`: The release date of the game.
   - `metacritic_score`: The game's score on Metacritic.
   - `developer_id`: Foreign key referencing the `developer` table.
   - `publisher_id`: Foreign key referencing the `publisher` table.
   - `review_summary_id`: Foreign key referencing the `review_summary` table.

2. **developer**: This table stores information about game developers.
   - `developer_id`: Primary key, an integer uniquely identifying the developer.
   - `name`: The name of the developer.

3. **publisher**: This table stores information about game publishers.
   - `publisher_id`: Primary key, an integer uniquely identifying the publisher.
   - `name`: The name of the publisher.

4. **review_summary**: This table stores review summaries for games.
   - `review_summary_id`: Primary key, an integer uniquely identifying the review summary.
   - `summary`: The review summary text.

5. **genre**: This table stores information about game genres.
   - `genre_id`: Primary key, an integer uniquely identifying the genre.
   - `name`: The name of the genre.

6. **game_genre**: This table is a many-to-many relationship table between games and genres.
   - `game_id`: Foreign key referencing the `game` table.
   - `genre_id`: Foreign key referencing the `genre` table.

7. **price_history**: This table stores the price history of games.
   - `price_history_id`: Primary key, an integer uniquely identifying the price history entry.
   - `game_id`: Foreign key referencing the `game` table.
   - `price`: The price of the game at the time of the sample.
   - `currency`: The currency of the price (e.g., USD, EUR, etc.).
   - `sample_date`: The date when the price was sampled.

8. **top_selling_history**: This table stores the history if games' positions top-selling chart of a particular category.
   - `top_selling_history_id`: Primary key, an integer uniquely identifying the top-selling history entry.
   - `game_id`: Foreign key referencing the `game` table.
   - `position`: The position of the game in the top-selling list.
   - `sample_date`: The date when the position was sampled.
   
9. **twitter**: This table contains information about number of mentions on Twitter for top ten games on a given date.
   - `game_id`: Foreign key referencing the `game` table.
   - `mentions_count`: Number of mentions for a game on a given query date.
   - `query date`: A date when the query sampling the number of mentions of a game om Twitter was made.

![steamgame_database_edr.png](/Users/Pleasantville/ITC_Studies/Python/webscraping/steam/steamgame_database_edr.png)

**The code to deploy and populate of the database using mysql.connector and SQLAlchemy is provided in detail in 
the files steam_sql_tables.py and steam_populate_database.py
