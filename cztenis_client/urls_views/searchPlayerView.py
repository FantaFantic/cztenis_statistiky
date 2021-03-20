from django.shortcuts import render
# own libraries
from cztenis_client.globalVariables import tenisScraperInstance

import pandas as pd
import json
import cztenis_client.globalVariables



loadedSearches = {}

def search_player(request, name):

    scraper = tenisScraperInstance

    # regular search: Last name first

    if(not(name in loadedSearches)):
        loadedSearches[name] = scraper.searchPlayer(name)

    found_players = loadedSearches[name]
    player_ids = []
    for player in found_players:
        player_ids.append(player.id)

    # # special search: Last name last

    name_array = name.split(" ")
    if(len(name_array) > 1):
        new_name = ""
        for i  in range (1, len(name_array)):
            new_name += name_array[i] + " "
        new_name += name_array[0] 

        other_found_players = scraper.searchPlayer(new_name)
        for player in other_found_players:
            if(player.id not in player_ids):
                found_players.append(player)
    
    if(len(found_players)>0):
        mylist = list(dict.fromkeys(found_players))
        found_players = mylist

        found_players.sort()
    
    if(len(found_players) ==0):
        found_players = None
        

    return render(request, 'searchResults.html', {"found_players" : found_players, "searched_name" : name})
