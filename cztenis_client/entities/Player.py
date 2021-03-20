
class Player():

    id = None
    full_name = None
    last_name = None
    date_of_birth = None
    club = None
    registration = None

    def __init__(self, id, full_name, last_name, date_of_birth, club, registration):
        self.id = id
        self.full_name = full_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.club = club
        self.registration = registration


    def __str__(self):
        return ("[%s] %s, %s, %s" % (self.id, self.full_name, self.date_of_birth, self.club))


    def __lt__(self,other):
        return self.last_name<other.last_name
