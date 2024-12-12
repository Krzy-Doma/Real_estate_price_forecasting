import joblib
import mapbox
import pandas as pd
from xgboost import XGBRegressor
from PropertyInput import PropertyInput


class PriceEstimator:

    data = pd.read_csv('models/cleaned_district_changed2.csv', sep='|')
    city_districts = data['city_district'].value_counts().to_dict()

    def __init__(self):
        self.geocoder = mapbox.Geocoder(
            access_token='pk.eyJ1Ijoia3J6eWRvbWEiLCJhIjoiY2x6cXVnajM3MXFxZTJscXdzZW8wZDI5eSJ9.72R-bCPXUFTSAqp7sY1BHw')
        self.models = {
            "Random Forest": joblib.load('models/random_forest_model.pkl'),
            "Gradient Boosting": joblib.load('models/gradient_boost.pkl'),
            "XGB": joblib.load('models/XGB.pkl')
        }
        self.preprocessor = joblib.load('models/preprocessor.pkl')

    def get_coordinates(self, city: str, district: str):
        place = self.geocoder.forward(f"{city} {district}")
        features = place.geojson()['features']
        return features[0]['geometry']['coordinates']

    def preprocess_input(self, property: PropertyInput, coordinates: list):
        column_names = [
            "area", "number_of_rooms", "floor", "type_of_market", "parking",
            "elevator", "year_of_creation", "internet", "type_of_building",
            "basement", "balcony", "garden", "terrace", "district",
            "city", "latitude", "longtitude", "city_district"
        ]
        row = [
            property.area, property.number_of_rooms, property.floor, property.type_of_market, property.parking,
            property.elevator, property.year_of_creation, property.internet, property.type_of_building,
            property.basement, property.balcony, property.garden, property.terrace, property.district,
            property.city, coordinates[1], coordinates[0], f"{property.city}_{property.district}"
        ]
        df = pd.DataFrame([row], columns=column_names)
        df['city_district'] = df['city_district'].map(self.city_districts)
        return self.preprocessor.transform(df)

    def estimate_price(self, property: PropertyInput):
        coordinates = self.get_coordinates(property.city, property.district)
        preprocessed = self.preprocess_input(property, coordinates)
        return self.models[property.model].predict(preprocessed)[0]
