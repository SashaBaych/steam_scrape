class SteamGameCatalog(dict):
    """
    A custom dictionary subclass to store and manage a collection of SteamGame objects.
    """

    def __init__(self, category):
        self.category = category

    def add_game(self, rank=None, name=None, link=None, source=None, info=None):
        """
        Adds a new SteamGame object to the catalog or updates an existing one with new data.

        Args:
            rank (int, optional): The game's rank.
            name (str, optional): The game's name.
            link (str, optional): The game's link.
            source (str, optional): The game's web source.
            info (dict, optional): A dictionary containing additional game information.

        Returns:
            SteamGame: The created or updated SteamGame object.
        """
        if name not in self:
            game = SteamGame(rank, name, self.category, link, source, info)
            self[name] = game
        else:
            # Update the existing game object with new data
            self.update_game(rank, name, self.category, link, source, info)

        return self[name]

    def update_game(self, name, rank=None, category=None, link=None, source=None, info=None):
        """
        Updates an existing SteamGame object with new data.

        Args:
            name (str): The name of the game to update.
            rank (int, optional): The game's rank.
            link (str, optional): The game's link.
            source (str, optional): The game's web source.
            info (dict, optional): A dictionary containing additional game information.
        """
        if name in self:
            game = self[name]
            game.rank = rank
            game.category = category
            game.link = link
            game.web_source = source
            game.info = info

    def get_game(self, name):
        """
        Retrieves a SteamGame object by its name.

        Args:
            name (str): The name of the game to retrieve.

        Returns:
            SteamGame: The SteamGame object with the specified name, or None if not found.
        """
        return self.get(name)

    def get_all_games(self):
        """
        Returns a string representation of the SteamGameCatalog.

        Returns:
            str: A string representation of the SteamGameCatalog with each game on a new line.
        """
        return self.values()

    def __str__(self):
        output = ''
        for key, value in self.items():
            output += str(value) + "\n"
        return output


class SteamGame:
    """
    A class to store and manage information about a Steam game.
    """
    def __init__(self, rank=None, name=None, category=None, link=None, source=None, info=None):
        """
        Initializes a SteamGame object with the provided data.

        Args:
            rank (int, optional): The game's rank.
            name (str, optional): The game's name.
            link (str, optional): The game's link.
            source (str, optional): The game's web source.
            info (dict, optional): A dictionary containing additional game information.
        """
        self.rank = rank
        self.name = name
        self.category = category
        self.link = link
        self.web_source = source
        self.info = info

    def __str__(self):
        output = f"rank: {self.rank}\nname: {self.name}\ncategory: {self.category}"
        if self.info:
            for key, value in self.info.items():
                if key != 'name':
                    output += f"\n{key}: {value}"
        return output + "\n"
