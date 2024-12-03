import random
import joblib
import mapbox
import pandas as pd
from xgboost import XGBRegressor
from PropertyInput import PropertyInput


class PriceEstimator:
    def __init__(self):
        self.geocoder = mapbox.Geocoder(
            access_token='pk.eyJ1Ijoia3J6eWRvbWEiLCJhIjoiY2x6cXVnajM3MXFxZTJscXdzZW8wZDI5eSJ9.72R-bCPXUFTSAqp7sY1BHw')
        self.models = {
            "Random Forest": joblib.load('random_forest_model.pkl'),
            "Gradient Boosting": joblib.load('gradient_boost.pkl'),
            "XGB": joblib.load('XGB.pkl')
        }
        self.preprocessor = joblib.load('preprocessor.pkl')

    def get_coordinates(self, city: str, district: str):
        place = self.geocoder.forward(f"{city} {district}")
        features = place.geojson()['features']
        return features[0]['geometry']['coordinates']

    def preprocess_input(self, property: PropertyInput, coordinates: list):
        column_names = [
            "area", "number_of_rooms", "floor", "type_of_market", "parking",
            "elevator", "year_of_creation", "internet", "type_of_building",
            "basement", "balcony", "garden", "terrace", "district",
            "city", "latitude", "longtitude"
        ]
        row = [
            property.area, property.number_of_rooms, property.floor, property.type_of_market, property.parking,
            property.elevator, property.year_of_creation, property.internet, property.type_of_building,
            property.basement, property.balcony, property.garden, property.terrace, property.district,
            property.city, coordinates[1], coordinates[0]
        ]
        df = pd.DataFrame([row], columns=column_names)
        return self.preprocessor.transform(df)

    def estimate_price(self, property: PropertyInput):
        coordinates = self.get_coordinates(property.city, property.district)
        if property.model == "Gradient Boosting":
            preprocessed = self.preprocess_input(property, coordinates)
            return self.models["Gradient Boosting"].predict(preprocessed)[0]
        elif property.model == "Random Forest":
            preprocessed = self.preprocess_input(property, coordinates)
            return self.models["Random Forest"].predict(preprocessed)[0]
        elif property.model == "XGB":
            preprocessed = self.preprocess_input(property, coordinates)
            return self.models["XGB"].predict(preprocessed)[0]
        else:
            return 10
