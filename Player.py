

'''
above this: players = { name : Player }
Player = { name : gamesToElo }  - kinda not necessary? { name : gamesToElo { game : elo }} 
    so cut out the redundant and unnecessary name in the middle?
gamesToElo = { game : Elo }   
so to search one needs a name (to get the player) and a game (to get the elo for a certain game)
'''


class Player():

    
    def __init__(self, name, game):
        self.name = name    # for faster searching down the line -?
        self.gamesToElo = {}
        self.playerToGame = { name : self.gamesToElo }
        self.gamesToElo.update( {game : 1500} )

    def getFromName(self):
        return self.gamesToElo

    def getFromGame(self, game):
        return self.gamesToElo.get(game)
