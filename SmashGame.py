
'''

'''

class SmashGame():
    #def __init__(self) -> None:    add function annotations
        #pass

    def __init__(self, url):
        self.playerEloDictionary = {}   #maybe want this as a global variable so a player can have many entries for different games
        self.gameTabs = 2   #this will need to be the return value of a function