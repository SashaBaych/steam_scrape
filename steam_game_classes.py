class SteamGameCatalog(dict):
    def create_game(self, rank=None, name=None, link=None, source=None, info=None):
        if name not in self:
            game = SteamGame(rank, name, link, source, info)
            self[name] = game
        else:
            # Update the existing game object with new data
            self.update_game(rank, name, link, source, info)

        return game

    def update_game(self, name, rank=None, link=None, source=None, info=None):
        if name in self:
            game = self[name]
            game.rank = rank
            game.link = link
            game.web_source = source
            game.info = info

    def get_game(self, name):
        return self.get(name)

    def get_all_games(self):
        return self.values()

    def __str__(self):
        output = ''
        for key, value in self.items():
            output += str(value) + "\n"
        return output



class SteamGame:
    def __init__(self, rank=None, name=None, link=None, source=None, info=None):
        self.rank = rank
        self.name = name
        self.link = link
        self.web_source = source
        self.info = info

    def __str__(self):
        return f"{self.rank}, {self.name}, {self.link})"
