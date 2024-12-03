class Property:
    def __init__(self, area=50.0, number_of_rooms=2, floor='0', city='default', district='default', year_of_creation=2000,
                 type_of_market="primary", type_of_building="Apartment", parking=False, internet=False, basement=False, balcony=False,
                 garden=False, terrace=False, elevator=False):
        self.area = area
        self.number_of_rooms = number_of_rooms
        self.floor = floor
        self.city = city
        self.district = district
        self.year_of_creation = year_of_creation
        self.type_of_market = type_of_market
        self.type_of_building = type_of_building
        self.parking = parking
        self.internet = internet
        self.basement = basement
        self.balcony = balcony
        self.garden = garden
        self.terrace = terrace
        self.elevator = elevator

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)