class Future_tournament:

    link = None # odkaz

    tournament_name = None
    place = None # Březnice např

    

    date = None # datum

    gender = None
    category = None ## A / B / C / D / P
    id = None   # id akce


    def __init__(self, gender, date, id, name_place_string, link):
     
        self.gender = gender
        self.date = date

        self.id = id

        self.place = name_place_string

        splitt_array = str(name_place_string).split("<br/>")
        if(len(splitt_array) > 1):
            # has name
            self.tournament_name = splitt_array[0].split("<td>")[1]
            self.place = splitt_array[1].split(" (")[0]
            self.category = splitt_array[1].split(" (")[1].split(")")[0]

        else:
            self.tournament_name = ""
            self.place = splitt_array[0].split("<td>")[1].split(" (")[0]
            self.category = splitt_array[0].split("<td>")[1].split(" (")[1].split(")")[0]


        

        # name_array = name_place_string.split("\n")
        # if(len(name_array) > 1):
        #     self.tournament_name =  name_array[0]
        #     self.place = name_array[1].split(" (")[0]
        #     self.category = name_array[1].split(" (")[1][0]
        # else:
        #     self.place = name_place_string.split(" (")[0]
        #     self.category = name_place_string.split(" (")[1][0]
            # self.tournament_name = ""
        
        self.link = link
        #print("%s - %s %s %s %s %s [%s]" % (self.gender, self.date, self.id, self.tournament_name, self.place, self.link, self.category))