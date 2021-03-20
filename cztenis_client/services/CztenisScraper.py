# extern libraries
import requests as rq
from bs4 import BeautifulSoup


# own libraries
from cztenis_client.entities.Player import Player
from cztenis_client.entities.Ranking import Ranking
from cztenis_client.entities.Competition_category import Competition_category
from cztenis_client.entities.Tournament import Tournament
from cztenis_client.entities.Match import Match
from cztenis_client.entities.Future_tournament import Future_tournament
###     Na někdy: ->>no cache for get / post
#request = rq.get(self.current_player_id, headers={'Cache-Control': 'no-cache', "Pragma": "no-cache"})
###


class CztenisScraper:

    

    # static attributes:
    url = "http://cztenis.cz/"
    
    #categories = ["ml. žactvo", "st. žactvo", "dorost", "dospělí"]

    form_data = {"volba": 1, "sezona": 0} # for post method in get player matches
    

    current_player_id = ""

    categories = None    

    # Constructor
    # def __init__(self):
    #     number = 1


    def setPlayer(self, player_id):
        self.current_player_id = player_id


#######################                         #####           ##########
### TEMPLATE #####      #####           #####           #####   ###
##################              #####                           #######
                                                                ###
    def getPageTemplate(self):                                  ###
        request = rq.get(self.url + "hrac/"+ self.current_player_id)
        request.encoding = "utf-8"
        html_response = request.text
        soup = BeautifulSoup(html_response, "html.parser")

        #### data starting here :::: 
        all_tables = soup.findAll("table")

        table1_rows = all_tables.findNext("tr")
        ### et catara

    def get_future_tournaments_by_category(self, category):
        #form_data = {"hledejhrace": 1, "hledej": searchedText}
       
        request = rq.get(self.url + category + "/jednotlivci")
        request.encoding = "utf-8"
        html_response = request.text

        skip_second_row = False
        if(category == "babytenis" or category == "minitenis"):
            skip_second_row = True

        soup = BeautifulSoup(html_response, "html.parser")

        #### data starting here :::: 
        all_tables = soup.findAll("table")
        all_rows = all_tables[0].findAll("tr")

        all_tournaments = []

        # print(len(all_rows))
        # print("\n")
        count = 0
        for i in range (2, len(all_rows)):
            row = all_rows[i]
            columns = row.findAll("td")
            # print(row)
            # muži


            if(len(columns[0].text) != 1):
                all_tournaments.append(Future_tournament("muži", columns[0].text, columns[1].text, columns[2], columns[3].find("a")["href"]))
           
            # ženy
            if(not skip_second_row and len(columns[6].text) != 1):
                all_tournaments.append(Future_tournament("ženy", columns[6].text, columns[7].text, columns[8], columns[9].find("a")["href"])) 

        # print("je tu %s turnajů" % len(all_tournaments))

        return all_tournaments



##################################################################################################################################
#           SEARCH Players 
##################################################################################################################################
    def searchPlayer(self, searchedText):
        
        form_data = {"hledejhrace": 1, "hledej": searchedText}

        request = rq.post(self.url + "hrac/", form_data)
        request.encoding = "utf-8"
        html_response = request.text

        soup = BeautifulSoup(html_response, "html.parser")

        #### data starting here :::: 
        all_tables = soup.findAll("table")

        output_players = []

        for table in all_tables:

            current_rows = table.findAll("tr")

            for index in range(1, len(current_rows)):
                current_row_columns = current_rows[index].findAll("td")
                full_name = ""
                name_parts = current_row_columns[0].text.split(" ")
                last_name = name_parts[0]
                for i in range(1, len(name_parts)):
                    full_name += "%s " % name_parts[i]
                full_name += last_name

                try:
                    birth_date = current_row_columns[1].text
                except:
                    break
                output_players.append(Player(current_rows[index].find("a")["href"].split("/")[2], full_name, last_name, current_row_columns[1].text, current_row_columns[2].text, current_row_columns[3].text))
                
                #Player(id, full_name, last_name, date_of_birth, club, registration):
        
                #current_player = Player(home_players[index].find("a")["href"].split("/"[2]), )
       
        return output_players




##################################################################################################################################
#           GET Player info ::: 
##################################################################################################################################
    def getPlayerInfo(self):

        
        request = rq.get(self.url + "hrac/" + self.current_player_id)
        request.encoding = "utf-8"
        html_response = request.text
        soup = BeautifulSoup(html_response, "html.parser")
        try:
            player_info_table = soup.find("table")
            table_cells = player_info_table.findAll("td")
            registration_limit_date = table_cells[3].text
            home_club = table_cells[5].text
        except:
            return None

        birth_date = table_cells[1].text
        full_name_html = soup.find("h2")
        name_array = full_name_html.text.split(" ")
        name_length = len(name_array)
        last_name = name_array[0]
        full_name = ""
        for i  in range(1, name_length):
            full_name +="%s " % name_array[i]
        full_name += last_name

        
        return Player(self.current_player_id, full_name, last_name, birth_date, home_club, registration_limit_date)



##################################################################################################################################
#           GET RANKINGS ::: 
##################################################################################################################################

    def getPlayerRankings(self):
        request = rq.get(self.url + "hrac/" + self.current_player_id)
        request.encoding = "utf-8"
        html_response = request.text
        soup = BeautifulSoup(html_response, "html.parser")
        player_info_table = soup.find("table")
        ranking_table = player_info_table.findNext("table")
        rows = ranking_table.findAll("tr")
        categories = ["Mladší žactvo", "Starší žactvo", "Dorost", "Dospělí"]
        output = []
        for i in range (1, len(rows)):

            columns = rows[i].findAll("td")
            # print(columns[0])
            year = columns[0].text
            try:
                club = columns[1].text
            except: 
                return None
            #year, club, category, ranking, BH):
            for k in range (2, len(columns)):
                if("(" in columns[k].text):
                    rank = columns[k].text.split(" (")[0]
                    bh = columns[k].text.split(" (")[1].replace(")", "")
                    output.append(Ranking(year, club, categories[k-2], rank, bh))


        return output



##################################################################################################################################
#           GET MATCHES ::: 
##################################################################################################################################
    def getAllTournamentsInYearRange(self, beginning_year, ending_year):
        output = []
        for year in range (beginning_year, ending_year+1):
            print("loading year: ", year)
            output += self.getAllTournamentsByYear(year)
        return output


    def loadCurrentPageCategories(self, page):
        categories = page.findAll("h3")
        self.categories = []
        for part in categories:
            self.categories.append(Competition_category(part.text))

    # Tournament[] -> Tournament has Match[] inside
    def getAllTournamentsByYear(self, year):

        # request
        self.form_data["sezona"] = year
        request = rq.post(self.url + "hrac/"+self.current_player_id, self.form_data)
        request.encoding = "utf-8"
        html_response = request.text

        soup = BeautifulSoup(html_response, "html.parser")
        # // request

        # load categories on this page -> need the order to parse out matches
        self.loadCurrentPageCategories(soup)


        current_index = 0
        current_tournaments = []
        tables = soup.findAll("table")
        k = 0
        for i in range (2, len(tables)):


            string_table = str(tables[i])
            

            rows = tables[i].findAll("tr")
        
            current_tournament = None

            if(rows[0].text[0] == '#'):
                if(i > 3):
                    current_index +=1
                continue
            else:
                if(i % 2 == 0):
                    current_tournament = Tournament(rows[0], self.categories[current_index+0], self)
                        
                else:
                    current_tournament = Tournament(rows[0], self.categories[current_index+1], self)

                
            if(len(rows) > 2):
                for row_number in range(1, len(rows)):
            # print("INdex : %d, current index: %d" % (i, current_index))
                    if(len(rows) > row_number + 1 and len(rows[row_number]) > 2):
                        if(current_tournament.category_type.category_type == "družstva"):
                            current_match = Match(current_tournament.category_type,  rows[row_number], current_tournament.home_team, current_tournament.host_team, current_tournament.home_team_link, current_tournament.host_team_link)
                        else:
                            current_match = Match(current_tournament.category_type, rows[row_number])
                        
                        current_tournament.addMatch(current_match)
                    else:
                        # print("body: %s\n" % rows[row_number])
                        
                        gained_points = rows[row_number].find("strong").text.split(": ")[1].split(" b")[0]
                        if(gained_points != ""):
                            current_tournament.setPoints(gained_points)
                        else:
                            
                            current_tournament.setPoints(0)

                current_tournaments.append(current_tournament)

        # sort by date ... :) ->bcs družstva
        current_tournaments.sort(key=lambda tournament: tournament.date)
        

        return current_tournaments