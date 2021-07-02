import requests
from bs4 import BeautifulSoup

class Bracket():

    GREENCHECK = '/commons/images/6/66/GreenCheck.png'
    
    def __init__(self, url, parent):    # parent might not be needed
        self.indices = [0, 0, 0]
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

    def containsBracket(self, name):
        return name and 'bracket column bracket-column-matches' in name

