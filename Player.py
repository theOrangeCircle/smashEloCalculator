

class Player():

    #lots of overhead memory for not so many players that swap over - make each on the fly
    def __init__(self, name):
        self.name = name
        self.gamesToElo = []
        self.playerToGame = { name : self.gamesToElo }

    '''
    creates a default elo for a given game for a given player
        game = string name of the game
        name = string name of the player?
    '''
    def addNewGameForPlayer(self, name, game):
        gameToElo = { game : 1500 }
        