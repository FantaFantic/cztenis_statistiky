
import datetime

class Tournament:

    scraper_link = None

    date = None
    date_string = None
    tournament_place = None
    
    matches = None

    points = None

    competition_link = None
    competition_type = None

    home_team_link  = None
    home_team = None
    host_team_link = None
    host_team = None
    

    date_format = "%d.%m.%Y"

    exception_date = "%d.%m."



    def parseDruzstva(self, input):
        input_a = input.findAll("a")
        
        self.date_string = input_a[0].text.split(", ")[0].split(" ")[0]

        try:
            self.date = datetime.datetime.strptime(self.date_string, self.date_format)
        except:
            try:
                self.date = datetime.datetime.strptime(self.date_string, self.exception_date)
                self.date.year = self.scraper_link.form_data["sezona"]
                self.date_string += self.scraper_link.form_data["sezona"]
            except:
                self.date = datetime.datetime(int(self.scraper_link.form_data["sezona"]), 1,1)
                self.date_string = "1.1." + self.scraper_link.form_data["sezona"]
        

        self.competition_link = input_a[0]["href"]
        self.competition_type = input_a[0].text.split(", ")[1]

        self.home_team_link = input_a[1]["href"]
        self.home_team = input_a[1].text
        self.tournament_place = self.home_team
        self.host_team_link = input_a[2]["href"]
        self.host_team = input_a[2].text
    
    def parseJednotlivci(self, input):

        

        input_lane = str(input)
        tournament_text = input.find("h4").text

        self.competition_link = input.find("a")["href"]

        self.tournament_place = tournament_text.split(" (")[0]
        self.date_string = input_lane.split(">")[3].split("<")[0].split(",")[0]

        try:
            self.date = datetime.datetime.strptime(self.date_string, self.date_format)
        except:
            try:
                self.date = datetime.datetime.strptime(self.date_string, self.exception_date)
                self.date.year = self.scraper_link.form_data["sezona"]
                self.date_string += self.scraper_link.form_data["sezona"]
            except:
                self.date = datetime.datetime(int(self.scraper_link.form_data["sezona"]), 1,1)
                self.date_string = "1.1." + self.scraper_link.form_data["sezona"]

        
        try:
            self.competition_type = tournament_text.split(" (")[1].split("),")[0].split(" -")[0]
        except:
            self.competition_type = ""

    def __init__(self, input, category, scraper_link = None ):
        self.scraper_link = scraper_link
        self.category_type = category
        #print(category)

        if(category.category_type == "družstva"):
            self.parseDruzstva(input)
        else:
            self.parseJednotlivci(input)

        self.matches = []

    def setPoints(self, points):
        self.points = points

    def __str__(self):
    #     return '{"%s","%s","%s","%s","%s","%s","%s","%s","%s"}'%
    #      date = None
    # tournament_place = None
    
    # matches = None

    # points = None

    # competition_link = None
    # competition_type = None

    # home_team_link  = None
    # home_team = None
    # host_team_link = None
    # host_team = None
    

        if(self.category_type.category_type == "jednotlivci"):
            return "%s:\n[%s] %s (%s) [%s b]" % (self.category_type, self.date, self.tournament_place, self.competition_type, self.points)
        else:
            return "%s:\n[%s] %s vs %s (%s) [%s b]" % (self.category_type, self.date, self.home_team, self.host_team, self.competition_type, self.points)



    def addMatch(self, match):
        self.matches.append(match)

    def toJson(self):
        current_tournament = {}

        self.category_type

        current_tournament["category_type"] = {"category_type" : self.category_type.category_type, "age_category" : self.category_type.age_category, "play_type" : self.category_type.play_type, }


        current_tournament["date"] = self.date
        current_tournament["tournament_place"] = self.tournament_place
        
        current_tournament["matches"] = self.matches

        current_tournament["points"] = self.points

        current_tournament["competition_link"] = self.competition_link
        current_tournament["competition_type"] = self.competition_type

        current_tournament["home_team_link"] = self.home_team_link
        current_tournament["home_team"] = self.home_team
        current_tournament["host_team_link"] = self.host_team_link
        current_tournament["host_team"] = self.host_team

        current_tournament["matches"] = []

        return current_tournament