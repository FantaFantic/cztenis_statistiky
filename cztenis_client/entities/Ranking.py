class Ranking:

    year = None
    club = None
    category = None
    ranking = None
    BH = None

    active_seasons = [] ### years of seasons where > 0 tournaments
    points_per_season = [] ### points per season and category [2014] = {"dorost" : 15}


    def __init__(self, year, club, category, ranking, BH):
        self.year = year
        self.club = club
        self.category = category



        self. ranking = ranking
        self.BH = BH

    def __str__(self):
        return '["%s","%s","%s","%s","%s"]' % (self.year, self.club, self.category, self.ranking, self.BH)

    def toJson(self):
        output = {}
        output["year"] = self.year

        output["category"] = self.category

        output["ranking"] = self.ranking
        output["BH"] = self.BH

        return output




    
