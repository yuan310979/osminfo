import pickle

from pathlib import Path

class POI:

    def __init__(self):
        # C1: Vehicle Survice
        self.class1 =   [
                            ('amenity', 'fuel'),
                            ('amenity', 'bicycle_repair_station'),
                            ('amenity', 'vehicle_inspection'),
                            ('craft', 'car_repair')
                        ]

        # C2: Transportation spots
        self.class2 =   [
                            ('aeroway', 'aerodrome'),
                            ('amenity', 'bicycle_parking'),
                            ('amenity', 'bicycle_rental'),
                            ('amenity', 'boat_rental'),
                            ('amenity', 'boat_sharing'),
                            ('amenity', 'buggy_parking'),
                            ('amenity', 'bus_station'),
                            ('amenity', 'car_rental'),
                            ('amenity', 'car_sharing'),
                            ('amenity', 'charging_station'),
                            ('amenity', 'ferry_terminal'),
                            ('amenity', 'motorcycle_parking'),
                            ('amenity', 'parking'),
                            ('amenity', 'taxi'),
                            ('building', 'train_station'),
                            ('building', 'transportation'),
                            ('public_transportation', 'stop_position'),
                            ('public_transportation', 'platform'),
                            ('public_transportation', 'station'),
                            ('railway', 'halt'),
                            ('railway', 'stop_position'),
                            ('railway', 'station')
                        ]

        # C3: Factory
        self.class3 =   [
                            ('building', 'industrial'),
                            ('landuse', 'industrial'),
                            ('man_made', 'chimney'),
                            ('power', 'plant')
                        ]

        # C4: Decoration and Furniture Market
        self.class4 =   [
                            ('shop', 'antiques'),
                            ('shop', 'bed'),
                            ('shop', 'candles'),
                            ('shop', 'carpet'),
                            ('shop', 'curtain'),
                            ('shop', 'doors'),
                            ('shop', 'flooring'),
                            ('shop', 'furniture'),
                            ('shop', 'interior_decoration'),
                            ('shop', 'kitchen'),
                            ('shop', 'lamps'),
                            ('shop', 'tiles'),
                            ('shop', 'window_blind')
                        ]

        # C5: Food and Beverage
        self.class5 =   [
                            ('amenity', 'bar'),
                            ('amenity', 'cafe'),
                            ('amenity', 'fast_food'),
                            ('amenity', 'food_court'),
                            ('amenity', 'ice_cream'),
                            ('amenity', 'restaurant'),
                            ('shop', 'alcohol'),
                            ('shop', 'bakery'),
                            ('shop', 'beverages'),
                            ('shop', 'butcher'),
                            ('shop', 'cheese'),
                            ('shop', 'chocolate'),
                            ('shop', 'coffee'),
                            ('shop', 'confectionery'),
                            ('shop', 'convenience'),
                            ('shop', 'deli'),
                            ('shop', 'dairy'),
                            ('shop', 'farm'),
                            ('shop', 'frozen_food'),
                            ('shop', 'greengrocer'),
                            ('shop', 'health_food'),
                            ('shop', 'ice_cream'),
                            ('shop', 'pasta'),
                            ('shop', 'pastry'),
                            ('shop', 'seafood'),
                            ('shop', 'spices'),
                            ('shop', 'tea'),
                            ('shop', 'water')
                        ]
        # C6: Shopping malls and Supermarkets
        self.class6 =   [
                            ('building', 'retail'),
                            ('building', 'Supermarket'),
                            ('building', 'kiosk'),
                            ('shop', 'department_store'),
                            ('shop', 'general'),
                            ('shop', 'kiosk'),
                            ('shop', 'mall'),
                            ('shop', 'supermarket'),
                            ('shop', 'wholesale')
                        ]

        # C7: Sports
        self.class7 =   [
                            ('amenity', 'dive_centre'),
                            ('building', 'stadium'),
                            ('building', 'grandstand'),
                            ('leisure', 'sports_centre'),
                            ('leisure', 'playground'),
                            ('leisure', 'horse_riding'),
                            ('leisure', 'fitness_centre'),
                            ('leisure', 'dance'),
                            ('leisure', 'disc_golf_course'),
                            ('leisure', 'stadium'),
                            ('leisure', 'swimming_area'),
                            ('leisure', 'pitch'),
                            ("sport", "9pin"),
                            ("sport", "10pin"),
                            ("sport", "american_football"),
                            ("sport", "aikido"),
                            ("sport", "archery"),
                            ("sport", "athletics"),
                            ("sport", "australian_football"),
                            ("sport", "badminton"),
                            ("sport", "bandy"),
                            ("sport", "base"),
                            ("sport", "baseball"),
                            ("sport", "basketball"),
                            ("sport", "beachvolleyball"),
                            ("sport", "billiards"),
                            ("sport", "bmx"),
                            ("sport", "bobsleigh"),
                            ("sport", "boules"),
                            ("sport", "bowls"),
                            ("sport", "boxing"),
                            ("sport", "canadian_football"),
                            ("sport", "canoe"),
                            ("sport", "chess"),
                            ("sport", "cliff_diving"),
                            ("sport", "climbing"),
                            ("sport", "climbing_adventure"),
                            ("sport", "cockfighting"),
                            ("sport", "cricket"),
                            ("sport", "croquet"),
                            ("sport", "curling"),
                            ("sport", "cycling"),
                            ("sport", "darts"),
                            ("sport", "dog_racing"),
                            ("sport", "equestrian"),
                            ("sport", "fencing"),
                            ("sport", "field_hockey"),
                            ("sport", "free_flying"),
                            ("sport", "futsal"),
                            ("sport", "gaelic_games"),
                            ("sport", "golf"),
                            ("sport", "gymnastics"),
                            ("sport", "handball"),
                            ("sport", "hapkido"),
                            ("sport", "horseshoes"),
                            ("sport", "horse_racing"),
                            ("sport", "ice_hockey"),
                            ("sport", "ice_skating"),
                            ("sport", "ice_stock"),
                            ("sport", "judo"),
                            ("sport", "karate"),
                            ("sport", "karting"),
                            ("sport", "kitesurfing"),
                            ("sport", "korfball"),
                            ("sport", "lacrosse"),
                            ("sport", "model_aerodrome"),
                            ("sport", "motocross"),
                            ("sport", "motor"),
                            ("sport", "multi"),
                            ("sport", "netball"),
                            ("sport", "obstacle_course"),
                            ("sport", "orienteering"),
                            ("sport", "paddle_tennis"),
                            ("sport", "padel"),
                            ("sport", "parachuting"),
                            ("sport", "paragliding"),
                            ("sport", "pelota"),
                            ("sport", "racquet"),
                            ("sport", "rc_car"),
                            ("sport", "roller_skating"),
                            ("sport", "rowing"),
                            ("sport", "rugby_league"),
                            ("sport", "rugby_union"),
                            ("sport", "running"),
                            ("sport", "sailing"),
                            ("sport", "scuba_diving"),
                            ("sport", "shooting"),
                            ("sport", "skateboard"),
                            ("sport", "soccer"),
                            ("sport", "sumo"),
                            ("sport", "surfing"),
                            ("sport", "swimming"),
                            ("sport", "table_tennis"),
                            ("sport", "table_soccer"),
                            ("sport", "taekwondo"),
                            ("sport", "tennis"),
                            ("sport", "toboggan"),
                            ("sport", "volleyball"),
                            ("sport", "water_polo"),
                            ("sport", "water_ski"),
                            ("sport", "weightlifting"),
                            ("sport", "wrestling"),
                            ("sport", "yoga"),
                            ("sport", "Value"),
                            ("sport", "exchange"),
                            ("sport", "connection_point"),
                            ("sport", "service_device"),
                            ("sport", "data_center")
                        ]

        # C8: Parks
        self.class8 =   [
                            ('landuse', 'basin'),
                            ('landuse', 'farmland'),
                            ('landuse', 'foreset'),
                            ('landuse', 'farmyard'),
                            ('landuse', 'grass'),
                            ('landuse', 'greenfield'),
                            ('landuse', 'greenhouse_horticulture'),
                            ('landuse', 'meadow'),
                            ('landuse', 'orchard'),
                            ('landuse', 'plant_nursery'),
                            ('landuse', 'village_green'),
                            ('landuse', 'vineyard'),
                            ('leisure', 'dog_park'),
                            ('leisure', 'garden'),
                            ('leisure', 'park'),
                            ('leisure', 'nature_reserve')
                        ]

        # C9: Culture & Education
        self.class9 =   [
                            ('amenity', 'college'),
                            ('amenity', 'kindergarten'),
                            ('amenity', 'library'),
                            ('amenity', 'archive'),
                            ('amenity', 'school'),
                            ('amenity', 'music_school'),
                            ('amenity', 'driving_school'),
                            ('amenity', 'language_school'),
                            ('amenity', 'university'),
                            ('amenity', 'research_institute'),
                            ('amenity', 'arts_centre'),
                            ('amenity', 'fountain'),
                            ('amenity', 'planetarium'),
                            ('amenity', 'social_centre'),
                            ('amenity', 'studio'),
                            ('amenity', 'theatre'),
                            ('building', 'religious'),
                            ('building', 'cathedral'),
                            ('building', 'chapel'),
                            ('building', 'church'),
                            ('building', 'mosque'),
                            ('building', 'temple'),
                            ('building', 'synagogue'),
                            ('building', 'shrine'),
                            ('building', 'bakehouse'),
                            ('building', 'kindergarten'),
                            ('building', 'school'),
                            ('building', 'university'),
                            ('historic', 'aircraft'),
                            ('historic', 'aqueduct'),
                            ('historic', 'archaeological_site'),
                            ('historic', 'battlefield'),
                            ('historic', 'boundary_stone'),
                            ('historic', 'building'),
                            ('historic', 'cannon'),
                            ('historic', 'castle'),
                            ('historic', 'castle_wall'),
                            ('historic', 'church'),
                            ('historic', 'city_gate'),
                            ('historic', 'citywalls'),
                            ('historic', 'farm'),
                            ('historic', 'fort'),
                            ('historic', 'gallows'),
                            ('historic', 'highwater_mark'),
                            ('historic', 'locomotive'),
                            ('historic', 'manor'),
                            ('historic', 'memorial'),
                            ('historic', 'milestone'),
                            ('historic', 'monastery'),
                            ('historic', 'monument'),
                            ('historic', 'optical_telegraph'),
                            ('historic', 'pillory'),
                            ('historic', 'railway_car'),
                            ('historic', 'ruins'),
                            ('historic', 'rune_stone'),
                            ('historic', 'ship'),
                            ('historic', 'tank'),
                            ('historic', 'tomb'),
                            ('historic', 'wayside_cross'),
                            ('historic', 'wayside_shrine'),
                            ('historic', 'wreck'),
                            ('historic', 'yes')
                        ]

        # C10: Entertainment
        self.class10 =  [
                            ('amenity', 'gambling'),
                            ('amenity', 'brothel'),
                            ('amenity', 'stripclub'),
                            ('amenity', 'swingerclub'),
                            ('amenity', 'nightclub'),
                            ('amenity', 'casino'),
                            ('amenity', 'cinema'),
                            ('amenity', 'community_centre'),
                            ('leisure', 'adult_gaming_centre'),
                            ('leisure', 'amusement_arcade'),
                            ('leisure', 'dance'),
                            ('leisure', 'water_park')
                        ]
        # C11: Company
        self.class11 =  [
                            ('building', 'commercial'),
                            ("office", "accountant"),
                            ("office", "adoption_agency"),
                            ("office", "advertising_agency"),
                            ("office", "architect"),
                            ("office", "association"),
                            ("office", "charity"),
                            ("office", "company"),
                            ("office", "educational_institution"),
                            ("office", "employment_agency"),
                            ("office", "energy_supplier"),
                            ("office", "engineer"),
                            ("office", "estate_agent"),
                            ("office", "financial"),
                            ("office", "forestry"),
                            ("office", "foundation"),
                            ("office", "geodesist"),
                            ("office", "government"),
                            ("office", "guide"),
                            ("office", "insurance"),
                            ("office", "it"),
                            ("office", "lawyer"),
                            ("office", "logistics"),
                            ("office", "moving_company"),
                            ("office", "newspaper"),
                            ("office", "ngo"),
                            ("office", "notary"),
                            ("office", "parish"),
                            ("office", "political_party"),
                            ("office", "private_investigator"),
                            ("office", "property_management"),
                            ("office", "quango"),
                            ("office", "religion"),
                            ("office", "research"),
                            ("office", "surveyor"),
                            ("office", "tax"),
                            ("office", "tax_advisor"),
                            ("office", "telecommunication"),
                            ("office", "therapist"),
                            ("office", "travel_agent"),
                            ("office", "visa"),
                            ("office", "water_utility"),
                            ("office", "yes")
                        ]

        # C12: Hotels and real estate
        self.class12 =  [
                            ('building', 'apartments'),
                            ('building', 'farm'),
                            ('building', 'hotel'),
                            ('building', 'house'),
                            ('building', 'detached'),
                            ('building', 'residential'),
                            ('building', 'dormitory'),
                            ('building', 'static_caravan'),
                            ('building', 'cabin')
                        ]

    def trans_poi_class_to_dict(self):
        ret = {}
        for c1 in self.class1:
            ret[c1] = 1
        for c2 in self.class2:
            ret[c2] = 2
        for c3 in self.class3:
            ret[c3] = 3 
        for c4 in self.class4:
            ret[c4] = 4 
        for c5 in self.class5:
            ret[c5] = 5 
        for c6 in self.class6:
            ret[c6] = 6 
        for c7 in self.class7:
            ret[c7] = 7 
        for c8 in self.class8:
            ret[c8] = 8 
        for c9 in self.class9:
            ret[c9] = 9 
        for c10 in self.class10:
            ret[c10] = 10
        for c11 in self.class11:
            ret[c11] = 11
        for c12 in self.class12:
            ret[c12] = 12
        return ret

    def save_pickle(self, path, obj):
        path = Path(path)
        if not path.parent.exists():
            path.parent.mkdir()
        path.write_bytes(pickle.dumps(obj))

    def load_pickle(self, path):
        path = Path(path)
        return pickle.load(path.open('rb'))

if __name__ == '__main__':
    path = '../pickle_data/poi_mapping_dict.pickle'

    poi = POI()
    d = poi.trans_poi_class_to_dict()

    poi.save_pickle(path, d)
