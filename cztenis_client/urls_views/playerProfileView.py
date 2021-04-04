from django.shortcuts import render
# own libraries
from cztenis_client.services import CztenisScraper
from cztenis_client.globalVariables import tenisScraperInstance

import json
import cztenis_client.globalVariables

from django.utils import timezone

from django.http import HttpResponse

from cztenis_client.entities.Carreer_summary import Carreer_summary
from threading import Timer

loadedPlayers = {}

playersFullyLoaded = {}

# all_matches_by_player_id = {}

all_tournaments_by_player_id = {}

career_summaries_by_player_id = {}

seasons_per_player = {}

points_by_player = {}

import cztenis_client.urls_views.cztenisScraperView as loaded_data



def reset_loaded(id):
    
    all_tournaments_by_player_id.pop(id)
    playersFullyLoaded[id] = False
    
    career_summaries_by_player_id.pop(id)

    seasons_per_player.pop(id)

    points_by_player.pop(id)
                
    loadedPlayers.pop(id)
    loaded_data.loadedTournamentsPerPlayer.pop(id)
    playersFullyLoaded.pop(id)



def get_player(id):
    if(id not in loadedPlayers):
        scraper = tenisScraperInstance
        scraper.setPlayer(id)
        player = scraper.getPlayerInfo()
        loadedPlayers[id] = player
        return player
    else:
        return loadedPlayers[id]


def set_fully_loaded(request, id, bool_value):

    
    playersFullyLoaded[id] = bool_value
    if(bool_value == "false"):
        
        if(id in all_tournaments_by_player_id):
            all_tournaments_by_player_id.pop(id)
            playersFullyLoaded[id] = False
            
            career_summaries_by_player_id.pop(id)

            seasons_per_player.pop(id)

            points_by_player.pop(id)
                        
            loadedPlayers.pop(id)
            loaded_data.loadedTournamentsPerPlayer.pop(id)
            playersFullyLoaded.pop(id)


        
        return ""
    # calculate basic stats

    # # TODO
    # print("tady jsem")
    # print(loaded_data.loadedMatchesPerPlayer[id])



    tournaments_by_season = loaded_data.loadedTournamentsPerPlayer[id]
    all_matches = []
    all_tournaments = []

    print("season funguguju")

    for season in tournaments_by_season:
        for tournament in season:
            all_tournaments.append(tournament)
            for match in tournament.matches:
                all_matches.append(match)

    # for tournament in tournaments:
    #     print(tournament)
    #     # for match in tournament.matches:
    #     #     all_matches.append(match)

    
    all_tournaments_by_player_id[id] = all_tournaments

    carreer_summary = Carreer_summary()

    carreer_summary.matches_count = len(all_matches)

    carreer_summary.win_count = sum(match.match_result == "Vítězství" for match in all_matches)

    carreer_summary.lose_count = carreer_summary.matches_count -  carreer_summary.win_count

    try:
        carreer_summary.win_rate = int(carreer_summary.win_count / carreer_summary.matches_count * 10000) / 100
    except: 
        carreer_summary.win_rate = "?"

    first_ever_tournament = None
    last_ever_tournament = None
    if(len(all_tournaments) > 0):

        last_ever_tournament = all_tournaments[len(all_tournaments)-1]
        first_ever_tournament = all_tournaments[0]
        
        
        points_by_season = {}

        for tournament in all_tournaments:
            
            if(not id in seasons_per_player):
                    seasons_per_player[id] = []

            if(not tournament.date.year in points_by_season):
                points_by_season[tournament.date.year] = {}

                seasons_per_player[id].append(tournament.date.year)

            if(not tournament.category_type.age_category in points_by_season[tournament.date.year]):
                points_by_season[tournament.date.year][tournament.category_type.age_category] = 0


            points_by_season[tournament.date.year][tournament.category_type.age_category] += int(tournament.points)
                

        if(not id in points_by_player):
            points_by_player[id] = points_by_season

           
    carreer_summary.first_ever_tournament = first_ever_tournament
    
    carreer_summary.last_ever_tournament = last_ever_tournament
    # print("summary:")
    # print(points_by_player[id][2020])

    ## BODY COUNT
 
    
    career_summaries_by_player_id[id] = carreer_summary

    t = Timer(600, reset_loaded, [id])
    t.start() # after 30 seconds, "hello, world" will be printed
    
    return HttpResponse(
            #json.dumps(""),
            json.dumps("fully_loaded"),
            content_type="application/json"
        )



def player_rankings(request, id):
    
    player = get_player(id)

    if(id in playersFullyLoaded and playersFullyLoaded[id]):
        #print("fully loaded")

        active_seasons = []

        for i in range (career_summaries_by_player_id[id].first_ever_tournament.date.year, career_summaries_by_player_id[id].last_ever_tournament.date.year + 1):
            active_seasons.append(i)

        for item in loaded_data.loaded_rankings[id]:
            if(not int(item["year"]) in active_seasons):
                active_seasons.append(int(item["year"]))
        
        active_seasons.sort()
        #print(active_seasons)

        points_array = []
        for item in points_by_player[id]:
            for key in points_by_player[id][item]:
                points_array.append("%s,%s,%s" % (item, key, points_by_player[id][item][key]))

        return render(request, 'player/player_rankings.html', {"player" : player, "active_seasons" : active_seasons, "summary" : career_summaries_by_player_id[id] ,"rankings" : loaded_data.loaded_rankings[id], "points" : points_array, "requested_id" : id})

    return render(request, 'player/player_rankings.html', {"loading" : True, "player" : player, "requested_id" : id})


def player_season(request, id):

    player = get_player(id)

    
    if(id in playersFullyLoaded and playersFullyLoaded[id]):
        return render(request, 'player/player_season.html', {"player" : player, "summary" : career_summaries_by_player_id[id] ,"requested_id" : id})

    return render(request, 'player/player_season.html', {"loading" : True, "player" : player, "requested_id" : id})


def player_match_history(request, id):
    
    player = get_player(id)
    
    if(id in playersFullyLoaded and playersFullyLoaded[id]):
        return render(request, 'player/player_match_history.html', {"player" : player, "summary" : career_summaries_by_player_id[id],  "all_players": cztenis_client.entities.Match.all_players, "all_tournaments" : all_tournaments_by_player_id[id],"requested_id" : id})

    return render(request, 'player/player_match_history.html', {"loading" : True,  "player" : player, "requested_id" : id})


def player_H2H(request, id):
    
    player = get_player(id)

    
    if(id in playersFullyLoaded and playersFullyLoaded[id]):
        return render(request, 'player/player_H2H.html', {"player" : player, "summary" : career_summaries_by_player_id[id],  "all_players": cztenis_client.entities.Match.all_players, "all_tournaments" : all_tournaments_by_player_id[id],"requested_id" : id})
    return render(request, 'player/player_H2H.html', {"loading" : True,  "player" : player, "requested_id" : id})


def player_partners(request, id):
    
    player = get_player(id)
    
    if(id in playersFullyLoaded and playersFullyLoaded[id]):
        return render(request, 'player/player_partners.html', {"player" : player, "summary" : career_summaries_by_player_id[id],  "all_players": cztenis_client.entities.Match.all_players, "all_tournaments" : all_tournaments_by_player_id[id],"requested_id" : id})

    return render(request, 'player/player_partners.html', {"loading" : True,  "player" : player, "requested_id" : id})

def player_tournaments(request, id):
    
    player = get_player(id)
    
    if(id in playersFullyLoaded and playersFullyLoaded[id]):
        return render(request, 'player/player_tournaments.html', {"player" : player, "summary" : career_summaries_by_player_id[id] ,"requested_id" : id})


    return render(request, 'player/player_tournaments.html', {"loading" : True, "player" : player, "requested_id" : id})
