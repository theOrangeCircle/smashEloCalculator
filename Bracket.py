import requests
from bs4 import BeautifulSoup
import Player
import math


class Bracket():

    GREENCHECK = '/commons/images/6/66/GreenCheck.png'
    
    def __init__(self, url, game):    
        self.indices = [0, 0, 0]
        self.game = game
        self.findBracketRounds(url)

    def findBracketRounds(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        brackets = soup.find_all(class_='bracket-wrapper bracket-player')
        self.winnersRounds, self.loserRounds, self.finalRounds, self.otherRounds, self.fromWhere = [], [], [], [], []
        for bracket in brackets:
            id = self.findBracketName(bracket)
            if 'Winner' in id:
                self.winnersRounds.append(bracket)
            elif 'Loser' in id:
                self.loserRounds.append(bracket)
                self.fromWhereSearch(bracket)
            elif 'Final' in id:
                self.finalRounds.append(bracket)
            else:
                self.otherRounds.append(bracket.find_all(class_=self.containsBracket))
        if self.winnersRounds: self.winnersRounds = self.condense(self.winnersRounds)
        if self.loserRounds: self.loserRounds = self.condense(self.loserRounds)
        if self.finalRounds: self.finalRounds = self.condense(self.finalRounds)

    def findBracketName(self, bracket):
        for sibling in bracket.previous_siblings:
            if sibling.name == 'h2':
                return sibling.span.get('id')
        return ''

    # this finds and saves the objects that contain the connecting images between bracket columns
    # this is used later for if someone (that is now in losers) came from winners there is a certain combination of images to represent this
    # otherwise there are other patterns for normal loser matches that draw players from the previous losers round
    def fromWhereSearch(self, bracket):
        for part in bracket.find_all(class_='bracket-column'):
            if len(part['class']) != 1:
                continue
            self.fromWhere.append(part)

    # need to change the fromWhen tests to instead test that all LRX players [list] are found in LRX-1 (set)
    def run(self, players):
        if not self.winnersRounds and self.otherRounds:
            self.processLoneOtherRounds(players)   
            return

        self.bracketRound(self.winnersRounds, players, 0)   # always run winners round 1 first  [0,0,0] -> [1,0,0]
        firstLoser = self.findFirstLoser(self.winnersRounds[self.indices[0]])   # find loser in WR2 (who will be sent down to losers)
        loserRoundPlayers = self.findAllLoserRoundPlayers(self.loserRounds[self.indices[1]])

        while firstLoser in loserRoundPlayers:  
            self.bracketRound(self.winnersRounds, players, 0)
            firstLoser = self.findFirstLoser(self.winnersRounds[self.indices[0]])
            loserRoundPlayers = self.findAllLoserRoundPlayers(self.loserRounds[self.indices[1]])

        self.bracketRound(self.loserRounds, players, 1) # need to run loser round now

        while self.indices[2] < len(self.fromWhere):    # this might need to be changed
            if self.findFromWinnersBracket(self.fromWhere[self.indices[2]]):    
                self.bracketRound(self.winnersRounds, players, 0)
                self.bracketRound(self.loserRounds, players, 1)
                self.indices[2] += 1
            else:
                self.bracketRound(self.loserRounds, players, 1)
                self.indices[2] += 1
        
        while self.indices[1] < len(self.loserRounds):
            self.bracketRound(self.loserRounds, players, 1)

        self.quickrun(self.finalRounds, players)
        # for bracket in self.finalRounds:
        #     self.quickrun(bracket, players)  # need to make this a quickrun?

    
    '''
    runs a round within a bracket
        runs a round within a given bracket and then increments the round number
    '''
    def bracketRound(self, bracket, players, index):
        round = bracket[self.indices[index]]
        games = round.find_all(class_='bracket-game')
        for game in games:
            self.processSet(game, players)
        self.indices[index] += 1

    '''
    process a set - finds the names of each player, how many games they won/ lost, updates elo
        game - a 'bracket-game' object
        ex. processSet(winnersRound.find(class_='bracket-game'))
    '''
    def processSet(self, game, players):
        topPlayer = game.find(class_='bracket-player-top')
        bottomPlayer = game.find(class_='bracket-player-bottom')
        
        if topPlayer: topPlayerName = self.findName(topPlayer) 
        else: return
        if bottomPlayer: bottomPlayerName = self.findName(bottomPlayer)
        else: return

        self.verifyPlayer(players, self.game, topPlayerName)
        self.verifyPlayer(players, self.game, bottomPlayerName)

        topPlayerScore = self.findScore(topPlayer)
        bottomPlayerScore = self.findScore(bottomPlayer)

        for scoreA, scoreB in zip(topPlayerScore, bottomPlayerScore):
            self.eloCalc(players, topPlayerName, bottomPlayerName, [scoreA, scoreB])

    
    # add comments
    def eloCalc(self, players, topName, botName, scoreList):
        difference = scoreList[0] - scoreList[1]
        if difference == 0: return
        if difference < 0: self.updateElo(players, botName, topName, -1 * difference)
        else: self.updateElo(players, topName, botName, difference)

    def updateElo(self, players, winner, loser, difference):
        winnerElo = players.get(winner).getFromGame(self.game) 
        loserElo = players.get(loser).getFromGame(self.game)

        winnerK = self.getK(winnerElo)
        loserK = self.getK(loserElo)

        winnerRanking = 10 ** (winnerElo / 400)
        loserRanking = 10 ** (loserElo / 400)

        winnerExpected = winnerRanking / (winnerRanking + loserRanking)
        loserExpected = loserRanking / (loserRanking + winnerRanking)

        for x in range(difference):
            winnerRanking = winnerRanking + (winnerK * (1 - winnerExpected))
            loserRanking = loserRanking + (loserK * (0 - loserExpected))
        
        players.get(winner).getFromName().update({ self.game : 400 * math.log10(winnerRanking)})
        players.get(loser).getFromName().update({ self.game : 400 * math.log10(loserRanking)})


    def getK(self, elo):
        if elo < 2100: return 32
        elif elo < 2400: return 24
        else: return 16


    # add comments to talk about this
    def verifyPlayer(self, players, game, name):
        playerData = players.get(name, -1)
        if playerData == -1:
            playerObject = Player.Player(name, game)
            players.update( {name : playerObject} )   
        players.get(name, -1).getFromName().setdefault(game, 1500)
        
    # need to return lists for everything in case there is a bracket reset in GF
    def findScore(self, player):
        score = player.find_all(class_='bracket-score')
        scores = []
        if score[0].text == 'DQ' or score[0].text == 'FF': return [0,0]
        if score[0].text == '': 
            for child in score[0].descendants:
                src = child.attrs.get('src')
                if src == self.GREENCHECK:
                    return [2,0]    
            return [0,0]            
        if score is None:
            score = player.find(class_='mobile-only bracket-score')
            if score is not None:
                return [int(score.text), 0]
            return [0,0] # need to test with a class_='bracket-class-icon'   
        if len(score) == 1:
            return [int(score[0].text), 0]
        else:       # should never reach here - need to check why I had this earlier
            for i in score:
                scores.append(int(i.get_text()))
            return scores
    

    def findName(self, player):
        for child in player.children:
            if child == '\xa0':
                continue
            if child.text != '':
                return child.get_text().strip()
        return ''

    # this is not working
    def containsBracket(self, name):
        return name and 'bracket-column bracket-column-matches' in name

    def processLoneOtherRounds(self, players):
        for brackets in self.otherRounds:
            self.quickrun(brackets, players)


    # can maybe move a bit of this into a method - top of processSet
    def findFirstLoser(self, winnerRound):
        firstWinnerGame = winnerRound.find(class_='bracket-game')
        topPlayer = firstWinnerGame.find(class_='bracket-player-top')
        bottomPlayer = firstWinnerGame.find(class_='bracket-player-bottom')

        if topPlayer: topPlayerName = self.findName(topPlayer)
        else: return
        if bottomPlayer: bottomPlayerName = self.findName(bottomPlayer)
        else: return

        topPlayerScore = self.findScore(topPlayer)
        bottomPlayerScore = self.findScore(bottomPlayer)

        return (topPlayerName, bottomPlayerName)[topPlayerScore > bottomPlayerScore]


    # can also add part of this to another method
    def findAllLoserRoundPlayers(self, loserRound):
        players = set()
        games = loserRound.find_all(class_='bracket-game')
        for game in games:
            topPlayer = game.find(class_='bracket-player-top')
            bottomPlayer = game.find(class_='bracket-player-bottom')

            if topPlayer: topPlayerName = self.findName(topPlayer)
            else: return
            if bottomPlayer: bottomPlayerName = self.findName(bottomPlayer)
            else: return

            players.add(topPlayerName)
            players.add(bottomPlayerName)
        return players


    # might need to change my approach here
    def findFromWinnersBracket(self, column):
        temp = column.find(class_='bracket-line-bottomleft')
        if temp == None: return False # cannot find start of pattern
        forDe = temp.next_sibling
        forDeC = temp.next_sibling.get('class')
        if forDeC == None: return False # cannot find second half
        return temp.next_sibling['class'][0] == 'bracket-line-straight' 

    def condense(self, list):
        masterList = []
        for part in list:
            for bracket in part.find_all(class_=self.containsBracket):
                masterList.append(bracket)
        return masterList


    def quickrun(self, columns, players):
        for column in columns:
            games = column.find_all(class_='bracket-game')
            for game in games:
                self.processSet(game, players)