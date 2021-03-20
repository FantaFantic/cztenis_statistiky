class Competition_category:

    age_category = None        # dospělí / dorost atd
    category_type = None       # družstva / jednotlivci
    play_type = None           # dvouhra / čtyřha




    def __init__(self, input):
        input_array = input.split(" - ")
        self.age_category = input_array[0]       # dospělí / dorost atd
        self.category_type = input_array[1]      # družstva / jednotlivci
        self.play_type = input_array[2]          # dvouhra / čtyřha
    

    def __str__(self):
        return "%s, %s, %s" % (self.age_category, self.category_type, self.play_type)
