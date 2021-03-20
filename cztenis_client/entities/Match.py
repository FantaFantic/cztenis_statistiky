

all_players = {}


round_to_text = {
    
}


class Match():

    # players info
    partner_id = None

    opponent_id = None
    second_opponent_id = None

    partner_name = None

    opponent_name = None
    second_opponent_name = None

    
    # is on left in score board or right
    isHost = None
    
    # družstva info
    playing_for_team = None
    playing_against_team = None
    your_team_link = None
    opponent_team_link = None

    # match info
    match_round = None

    number_of_sets = None
    match_result = None
    sets_won = None
    sets_lost = None
    games_won_per_set = None
    games_lost_per_set = None

    def parseDouble(self, input_tds):

        opponent_id = None
        opponent_name = None



        second_opponent_id = None
        second_opponent_name = None

        partner_name = None
        partner_id = None
        # opponent is on right
        if(self.is_host):
            opponent_name = input_tds[3].findAll("a")[0].text
            opponent_id = input_tds[3].findAll("a")[0]["href"].split("/")[2]

            second_opponent_name = input_tds[3].findAll("a")[1].text
            second_opponent_id = input_tds[3].findAll("a")[1]["href"].split("/")[2]

            # partner:
            if(input_tds[1].find("a").find("strong")):
                # partner is the second a
                partner_name = input_tds[1].findAll("a")[1].text
                partner_id = input_tds[1].findAll("a")[1]["href"].split("/")[2]

            else:
                partner_name = input_tds[1].findAll("a")[0].text
                partner_id = input_tds[1].findAll("a")[0]["href"].split("/")[2]
        # opponent is on left
        else:
            opponent_name = input_tds[1].findAll("a")[0].text
            opponent_id = input_tds[1].findAll("a")[0]["href"].split("/")[2]

            second_opponent_name = input_tds[1].findAll("a")[1].text
            second_opponent_id = input_tds[1].findAll("a")[1]["href"].split("/")[2]

            # partner:
            if(input_tds[3].find("a").find("strong")):
                # partner is the second a
                partner_name = input_tds[3].findAll("a")[1].text
                partner_id = input_tds[3].findAll("a")[1]["href"].split("/")[2]

            else:
                partner_name = input_tds[3].findAll("a")[0].text
                partner_id = input_tds[3].findAll("a")[0]["href"].split("/")[2]

        # print("opponent: %s-%s" % (opponent_id, opponent_name))
        # print("opponent: %s-%s" % (second_opponent_id, second_opponent_name))
        # print("partner: %s-%s"% (partner_id, partner_name))
        
        if(not(opponent_id in all_players)):
            all_players[opponent_id] = opponent_name

        if(not(second_opponent_id in all_players)):
            all_players[second_opponent_id] = second_opponent_name

        if(not(partner_id in all_players)):
            all_players[partner_id] = partner_name


        self.opponent_id = opponent_id
        self.second_opponent_id = second_opponent_id
        self.partner_id = partner_id

        self.partner_name = partner_name

        self.opponent_name = opponent_name
        self.second_opponent_name = second_opponent_name

    def parseSingle(self, input_tds):
        

        opponent_id = None
        opponent_name = None

        # opponent is on right
        if(self.is_host):
            opponent_name = input_tds[3].find("a").text.split(" ")[0]
            opponent_id = input_tds[3].find("a")["href"].split("/")[2]
            number = 1
        # opponent is on left
        else:
            opponent_name = input_tds[1].find("a").text.split(" ")[0]
            opponent_id = input_tds[1].find("a")["href"].split("/")[2]
            
        if(not(opponent_id in all_players)):
            all_players[opponent_id] = opponent_name

        self.opponent_id = opponent_id
        self.opponent_name = opponent_name


    # družstva konstruktor
    def __init__(self, category_type, input, home_team = "null", host_team ="null", home_team_link = "null", host_team_link = "null"):


        input_tds = input.findAll("td")
        self.is_host = False

#        print("%d --- (%s)" % (len(input_tds), input_tds))

        if(input_tds[1].find("strong")):
            # player is on left  
            self.is_host = True
            
        if(category_type.category_type == "družstva"):
            
            if(self.is_host):
                self.playing_for_team = home_team
                self.your_team_link = home_team_link
                self.playing_against_team = host_team
                self.opponent_team_link = host_team_link

                
            else:
                self.playing_for_team = host_team
                self.playing_against_team = home_team
                self.your_team_link = host_team_link
                self.opponent_team_link = home_team_link
                

        else:
            self.match_round = input_tds[0].text
        
        if(category_type.play_type == "dvouhra"):
            self.parseSingle(input_tds)
        else:
            self.parseDouble(input_tds)

        self.parseScore(input_tds)


    def parseScore(self, input_tds):
        sets = str(input_tds[4].text).split(", ")
        self.match_result = "Neznámý"
        self.sets_won = 0
        self.sets_lost = 0
        self.games_won_per_set = []
        self.games_lost_per_set = []
        
        for current_set in sets:
            # is on left
            your_games = None
            opponent_games = None
            if("scr" in current_set):
                self.match_result = "Skreč"
                self.games_won_per_set.append("scr.")
                self.games_lost_per_set.append("scr.")
                break
            
            if("" == current_set):
                self.match_result = "Neznámý"
                self.games_won_per_set.append("")
                self.games_lost_per_set.append("")
                break

            if(self.is_host):
                
                your_games = current_set.split(":")[0]
                opponent_games = current_set.split(":")[1]
            else:
                your_games = current_set.split(":")[1]
                opponent_games = current_set.split(":")[0]

            if("(" in your_games):
                your_games = your_games.split(" (")[0]

            if("(" in opponent_games):
                opponent_games = opponent_games.split(" (")[0]

            self.games_won_per_set.append(your_games)
            self.games_lost_per_set.append(opponent_games)
            try:
                if(int(your_games) > int(opponent_games)):
                    self.sets_won += 1
                if(int(your_games) < int(opponent_games)):
                    self.sets_lost += 1
            except:
                number = 1
                
        if(self.sets_won > self.sets_lost and self.match_result != "Skreč"):
            self.match_result = "Vítězství"
        if(self.sets_won < self.sets_lost and self.match_result != "Skreč"):
            self.match_result = "Porážka"

        self.number_of_sets = self.sets_won + self.sets_lost

    def __str__(self):
        return "against %s =  %s:%s" % (all_players[self.opponent_id], self.sets_won, self.sets_lost)



    def toJson(self):

        match = {}

        match["partner_id"] = self.partner_id
        match["opponent_id"] = self.opponent_id
        match["second_opponent_id"] = self.second_opponent_id
        match["isHost"] = self.isHost
        match["playing_for_team"] = self.playing_for_team
        match["playing_against_team"] = self.playing_against_team
        match["your_team_link"] = self.your_team_link
        match["opponent_team_link"] = self.opponent_team_link
        match["match_round"] = self.match_round
        match["match_result"] = self.match_result
        match["sets_won"] = self.sets_won
        match["sets_lost"] = self.sets_lost
        match["games_won_per_set"] = self.games_won_per_set
        match["games_lost_per_set"] = self.games_lost_per_set
        return match