from bs4 import BeautifulSoup
import requests
import Tournament
import time

class SmashGame():
    def __init__(self, url, game):
        self.gameTabs = self.findGameTabs(url)
        self.game = game

    def findGameTabs(self, url) -> 'list':
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        allTabs = soup.find_all(class_='tabs-static')
        gameTabs = []
        if len(allTabs) == 3:
            for tab in allTabs[2].contents[0]:
                # if this finds no link then the current tab is active (which removes the href attribute)
                if tab.find('a').get('href') == None:
                    gameTabs.insert(0, url)
                else:
                    gameTabs.insert(0, 'https://liquipedia.net' + tab.find('a').get('href'))
        else:
            gameTabs.insert(0, url)
        return gameTabs

    def run(self, players) -> None:
        for tab in self.gameTabs:
            self.__run__(tab, players)

    def __run__(self, tab, players):
        time.sleep(3)
        page = requests.get(tab)
        soup = BeautifulSoup(page.content, 'html.parser')
        allTournaments = soup.find_all(class_='divRow')
        for tournament in reversed(allTournaments):
            tournamentUrl = 'https://liquipedia.net' + tournament.find('b').find('a').get('href')
            if 'Lima/2012' in tournamentUrl: continue   # TODO much later 
            print(tournamentUrl) # I want to see what is processing - can remove later
            Tournament.Tournament(tournamentUrl, players, self.game) #want to add a run() to tournament