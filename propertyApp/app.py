import streamlit as st
import Property
from DistrictNames import DISTRICTS
import requests
import pandas as pd
from PIL import Image

def render_title():
    st.title("Property price predictions")


class App:
    API_URL = "http://127.0.0.1:8000"

    def __init__(self):
        self.property = Property.Property()
        self.city = None
        self.model = None
        self.prediction = None
        self.metrics = {
            "Random Forest": pd.read_csv('models/random_forest_metrics.csv', delimiter='|'),
            "Gradient Boosting": pd.read_csv('models/gradient_boost_metrics.csv', delimiter='|'),
            "XGB": pd.read_csv('models/XGB_metrics.csv', delimiter='|')
        }
        self.feature = {
            "Random Forest": Image.open('models/random_forest_feature_importance.png'),
            "Gradient Boosting": Image.open('models/gradient_boost_importance.png'),
            "XGB": Image.open('models/XGB_importance.png')
        }

    def select_city_model(self):
        c = st.radio("City", options=['Gdynia', 'Gdańsk', 'Sopot'])
        self.city = c.lower() if c != 'Gdańsk' else 'gdansk'
        self.model = st.radio("Choose model", options=['Gradient Boosting', 'Random Forest', 'XGB'])

    def render_form(self):
        with st.form("property_form"):
            st.header("Property details form")

            district = st.selectbox("District", options=DISTRICTS[self.city])
            area = st.number_input("Area [sqm]", value=self.property.area, min_value=0.0, step=0.5)
            number_of_rooms = st.slider("Number of rooms", min_value=1, max_value=10,
                                        value=self.property.number_of_rooms)
            floor = st.radio("Floor", options=['0', '1-3', '4-7', '8+'])
            year_of_creation = st.number_input("Year of creation", value=self.property.year_of_creation, min_value=1900,
                                               max_value=2024, step=10)
            type_of_market = st.selectbox("Type of market", ["primary", "secondary"])
            type_of_building = st.selectbox("Type of building", ["Apartment", "House"])
            # Boolean attributes
            parking = st.checkbox("Parking", value=self.property.parking)
            internet = st.checkbox("Internet", value=self.property.internet)
            basement = st.checkbox("Basement", value=self.property.basement)
            balcony = st.checkbox("Balcony", value=self.property.balcony)
            garden = st.checkbox("Garden", value=self.property.garden)
            terrace = st.checkbox("Terrace", value=self.property.terrace)
            elevator = st.checkbox("Elevator", value=self.property.elevator)

            submitted = st.form_submit_button("Submit")
            if type_of_building == 'House':
                floor = '0'
            else:
                floor = floor
            if submitted:
                self.property.update(
                    area=area,
                    number_of_rooms=number_of_rooms,
                    floor=floor,
                    city=self.city,
                    district=district.lower(),
                    year_of_creation=year_of_creation,
                    type_of_market=type_of_market,
                    type_of_building=type_of_building,
                    parking=parking,
                    internet=internet,
                    basement=basement,
                    balcony=balcony,
                    garden=garden,
                    terrace=terrace,
                    elevator=elevator,
                )
                st.success("Form submitted!")
                self.send_request()

    def send_request(self):
        property_data = {
            "model": self.model,
            "area": self.property.area,
            "number_of_rooms": self.property.number_of_rooms,
            "floor": self.property.floor,
            "type_of_market": self.property.type_of_market,
            "parking": self.property.parking,
            "elevator": self.property.elevator,
            "year_of_creation": self.property.year_of_creation,
            "internet": self.property.internet,
            "type_of_building": self.property.type_of_building,
            "basement": self.property.basement,
            "balcony": self.property.balcony,
            "garden": self.property.garden,
            "terrace": self.property.terrace,
            "district": self.property.district,
            "city": self.city,
        }

        try:
            response = requests.post(f"{self.API_URL}/predict-price/", json=property_data)
            if response.status_code == 200:
                self.prediction = response.json()
                st.success(f"Estimated price: {self.prediction['estimated_price']:.2f} PLN")
            else:
                st.error(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            st.error(f"Connection Error: {e}")

    def render_prediction(self):
        if self.prediction:
            st.title(f"Estimated price of the property: {self.prediction['estimated_price']:.2f} PLN")
            st.subheader(f"Price per meter square: {(self.prediction['estimated_price']/self.property.area) :.2f} PLN")

            st.write("Model metrics:")

            transpose = self.metrics[self.model].T
            transpose.iloc[1] = transpose.iloc[1].apply(pd.to_numeric).round(4)

            st.dataframe(transpose,  use_container_width=True)

            st.image(self.feature[self.model], use_column_width=True)

            # st.subheader("Model Evaluation Metrics")
            # st.table(metrics)
            # st.subheader("Model Evaluation Metrics")
            # st.markdown("""
            #     <style>
            #     .metrics-table {
            #         width: 100%;
            #         border-collapse: collapse;
            #         margin: 10px 0;
            #         font-size: 18px;
            #         text-align: left;
            #     }
            #     .metrics-table th, .metrics-table td {
            #         border: 1px solid #ddd;
            #         padding: 8px;
            #     }
            #     .metrics-table th {
            #         background-color: #f4f4f4;
            #         font-weight: bold;
            #     }
            #     </style>
            #     <table class="metrics-table">
            #         <thead>
            #             <tr>
            #                 <th>Metric</th>
            #                 <th>Value</th>
            #             </tr>
            #         </thead>
            #         <tbody>
            #             <tr>
            #                 <td>RMSE</td>
            #                 <td>2274.926</td>
            #             </tr>
            #             <tr>
            #                 <td>R²</td>
            #                 <td>0.778</td>
            #             </tr>
            #             <tr>
            #                 <td>MAE</td>
            #                 <td>1411.982</td>
            #             </tr>
            #             <tr>
            #                 <td>MAPE</td>
            #                 <td>0.099</td>
            #             </tr>
            #         </tbody>
            #     </table>
            #     """, unsafe_allow_html=True)

    def run(self):
        render_title()
        self.select_city_model()
        self.render_form()
        self.render_prediction()


if __name__ == "__main__":
    App().run()
