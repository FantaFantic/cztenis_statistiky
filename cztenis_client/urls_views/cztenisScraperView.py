from django.shortcuts import render
# own libraries
from cztenis_client.services import CztenisScraper
from cztenis_client.globalVariables import tenisScraperInstance

import pandas as pd
import json
import cztenis_client.globalVariables
import datetime
from django.http import HttpResponse

scraper = cztenis_client.globalVariables.tenisScraperInstance


loaded_rankings = {}        # { "player_id" : Rankings[] }

loadedTournamentsPerPlayer = {} # { "player_id" : [Tournaments] }


# def is_player_loaded(id):
    
#     if(not(id in loadedPlayers)):
#         return False
#     return True


# def load_all(id):
    
#     scraper = tenisScraperInstance
#     scraper.setPlayer(id)
    
#     if(not(id in loadedPlayers)):
#         loadedPlayers[id] = scraper.getPlayerInfo()
    
#     if(not(id in loadedRankings)):
#         loadedRankings[id] = scraper.getPlayerRankings()

#     # matches = []
#     # if(not(id in loadedTournaments)):
#     #     loadedTournaments[id] = scraper.getAllTournamentsInYearRange(2003,datetime.datetime.now().year)
        
#     #     for tournament in loadedTournaments[id]:
#     #         for match in tournament.matches:
#     #             matches.append(match)


        
#     #     loadedMatches[id] = matches




def get_rankings(request, id):
    if(id in loaded_rankings):
        return HttpResponse(
                #json.dumps(""),
                json.dumps(loaded_rankings[id]),
                content_type="application/json"
            )

    scraper.setPlayer(id)
    rankings = scraper.getPlayerRankings()
    output = []
    if (rankings != None): 
        for ranking in rankings:
            output.append(ranking.toJson())
                
    loaded_rankings[id] = output

    return HttpResponse(
            #json.dumps(""),
            json.dumps(output),
            content_type="application/json"
        )


def get_one_season(request, id, season):
    # if(id in loadedTournamentsPerPlayer):
    #         return HttpResponse(
    #             #json.dumps(""),
    #             json.dumps("ok"),
    #             content_type="application/json"
    #         )
   
    

    scraper.setPlayer(id)
    tournaments = scraper.getAllTournamentsByYear(season)
    
    # if(id not in loadedMatchesPerPlayer):
    #     loadedMatchesPerPlayer[id] = []

    # output = []

    # for tournament in tournaments:

    #     current_tournament = tournament.toJson()

    #     for match in tournament.matches:
            
    #         current_match = match.toJson()

    #         current_tournament["matches"].append(current_match)

    #         loadedMatchesPerPlayer[id].append(current_match)
    #         print()

    #         # print(match)

    #     output.append(current_tournament)
    
    if(id not in loadedTournamentsPerPlayer):
        loadedTournamentsPerPlayer[id] = []
    

    loadedTournamentsPerPlayer[id].append(tournaments)
    
    # print(loadedTournamentsPerPlayer[id])

    return HttpResponse(
            #json.dumps(""),
            json.dumps("ok"),
            content_type="application/json"
        )



