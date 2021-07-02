import requests
from bs4 import BeautifulSoup





def run():
    baseUrl = 'https://liquipedia.net'
    metaUrl = 'https://liquipedia.net/smash/Portal:Tournaments/All'
    metaPage = requests.get(metaUrl)
    metaSoup = BeautifulSoup(metaPage.content, 'html.parser')

    '''
    this finds all tabs
    [0] will be Tournaments, Major Tournaments, and Misc Tournaments (do not want to select either of these)
    [1] will contain the specific smash game ([1][0][0] is all [1][0][1] is n64 [1][0][2] is melee)
        there is a strange [0] between all of these due to how the html is written -- double check
    [2] will give time period breakdowns for the game if they exist so for 64 [2] doesn't exist
        but for melee it has [2][0] = present and [2][1] = pre-2018
        will have to select melee ([1][0][2]) and then reload the page to even get this sublist
    '''
    allTabs = metaSoup.find_all(class_='tabs-static')
    for i, tab in enumerate(allTabs):
        if i == 0 or i == 2: continue
        else:
            for game in tab.contents[0]: #switch statement soon pls
                if game.get_text() == '64':
                    #n64
                    pass
                elif game.get_text() == 'Melee':
                    #melee
                    pass
                elif game.get_text() == 'Brawl':
                    #brawl
                    pass
                elif game.get_text() == 'Project M':
                    #projectM
                    pass
                elif game.get_text() == 'Wii u':
                    #wiiu
                    pass
                elif game.get_text() == 'Ultimate':
                    #ultimate
                    pass
                



if __name__ == "__main__":
    run()