from bs4 import BeautifulSoup
import requests
import Bracket


class Tournament():

    
    def __init__(self, url, players, game):
        self.game = game
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tabs = soup.find(class_=self.containsNavTabs)
        if tabs is not None:
            self.tabList = self.findTabs(tabs)
            for tab in self.tabList:
                if 'Bracket' in tab.get_text() or 'Top' in tab.get_text(): # I don't think this is necessary
                    Bracket.Bracket('https://liquipedia.net' + tab.find('a').get('href'), self.game).run(players)
                elif 'Pool' in tab.get_text():
                    pass


    def containsNavTabs(self, name):
        return name and 'nav nav-tabs navigation-not-searchable tabs' in name

    def findTabs(self, tabs):
        tabList = []
        for tab in tabs:
            if 'Single' in tab.get_text() or 'Top' in tab.get_text(): #double check if 'Top' works
                tabList.append(tab)
        return tabList