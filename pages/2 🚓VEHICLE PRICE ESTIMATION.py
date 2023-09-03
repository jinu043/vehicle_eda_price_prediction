import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from sklearn.tree import DecisionTreeRegressor


from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

import streamlit as st

st.set_page_config(layout="wide", page_icon=":car:")

@st.cache_data
def get_data():
    df = pd.read_csv("ml_data.csv")
    df1 = df.query('vehicle_price != "Ask for price"').copy()
    df2 = df1.query('vehicle_price <= 2000000').copy()
    return df2
df3 = get_data()

st.markdown('<h2 div style="text-align: center;"> <mark style = "background-color:#F3EBEC;color:darkred;font-weight:bold">CURRENT MARKET PRICE ESTIMATION OF USED CARS IN UAE</mark> </div>', unsafe_allow_html=True)
st.markdown(f'<h6 div style="text-align: justify;">As I mentioned in introduction about data, I have extracted key features of vehicle which will somehow effect\
 the price of used cars in UAE market. I have extracted data from Dubicars website dated in August`2023. I have used Decision Tree algorithm to predict the price of\
 vehicle since most of the feature are categorical type. However I haven`t used vehicle dealer as a feature, but it may effect the vehicle price. Due to insufficient\
 samples from each dealer I avoided dealer feature from the model. Therefore when you change the mileage, there will be a noise in the price for some\
 vehicles. As a preprocessing for categorical features I have been used LabelEncoder and MinMaxScaler to change the features to numerical data.\
 For price prediction, you can change the below features and see the price of vehicle in below. You can also see the model error as well in below. </div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    vehicle_make = st.selectbox("Vehicle Make", df3["vehicle_make"].unique().tolist())
with col2:
    vehicle_model = st.selectbox("Vehicle Model", df3.query(f'vehicle_make == "{vehicle_make}"')["vehicle_model"].unique().tolist())
with col3:
    vehicle_type = st.selectbox("Vehicle Type", df3.query(f'vehicle_make == "{vehicle_make}" and vehicle_model == "{vehicle_model}"')["vehicle_type"].unique().tolist())
with col4:
    vehicle_year = st.selectbox("Vehicle Year", df3.query(f'vehicle_make == "{vehicle_make}" and vehicle_model == "{vehicle_model}" and vehicle_type == "{vehicle_type}"')["vehicle_year"].unique().tolist())
with col5:
    vehicle_fuel = st.selectbox("Vehicle Fuel", df3.query(f'vehicle_make == "{vehicle_make}" and vehicle_model == "{vehicle_model}" and vehicle_type == "{vehicle_type}" and vehicle_year == {vehicle_year}')["vehicle_fuel"].unique().tolist())

df4 = df3.query(f'vehicle_make == "{vehicle_make}" and vehicle_model == "{vehicle_model}" and vehicle_type == "{vehicle_type}" and vehicle_year == {vehicle_year} and vehicle_fuel == "{vehicle_fuel}"')

col6, col7, col8, col9 = st.columns(4)

with col6:
    vehicle_wheel = st.selectbox("Vehicle Wheel", df4["vehicle_wheel"].unique().tolist())
with col7:
    vehicle_cylinder = st.selectbox("Vehicle Cylinder", df4.query(f'vehicle_wheel == "{vehicle_wheel}"')["vehicle_cylinder"].unique().tolist())
with col8:
    vehicle_spec = st.selectbox("Vehicle Spec", df4.query(f'vehicle_wheel == "{vehicle_wheel}" and vehicle_cylinder == "{vehicle_cylinder}"')["vehicle_spec"].unique().tolist())
df5 = df4.query(f'vehicle_wheel == "{vehicle_wheel}" and vehicle_cylinder == "{vehicle_cylinder}" and vehicle_spec == "{vehicle_spec}"')
with col9:
    vehicle_mileage = st.number_input("Vehicle Mileage", min_value=df5["vehicle_mileage"].min(), max_value=df5["vehicle_mileage"].max(), step=50)

leme = LabelEncoder()
leml = LabelEncoder()
levw = LabelEncoder()
levt = LabelEncoder()
levc = LabelEncoder()
levy = LabelEncoder()
levf = LabelEncoder()
levs = LabelEncoder()

input_cols = df3.drop(columns=["vehicle_price", "vehicle_dealer"]).columns.tolist()
enc_cols = df3.drop(columns=["vehicle_mileage", "vehicle_price", "vehicle_dealer"]).columns.tolist()
target_col = "vehicle_price"

le1 = leme.fit(df3["vehicle_make"])
le2 = leml.fit(df3["vehicle_model"])
le3 = levw.fit(df3["vehicle_wheel"])
le4 = levt.fit(df3["vehicle_type"])
le5 = levc.fit(df3["vehicle_cylinder"])
le6 = levy.fit(df3["vehicle_year"])
le7 = levf.fit(df3["vehicle_fuel"])
le8 = levs.fit(df3["vehicle_spec"])

df3["vehicle_make"] = le1.transform(df3["vehicle_make"])
df3["vehicle_model"] = le2.transform(df3["vehicle_model"])
df3["vehicle_wheel"] = le3.transform(df3["vehicle_wheel"])
df3["vehicle_type"] = le4.transform(df3["vehicle_type"])
df3["vehicle_cylinder"] = le5.transform(df3["vehicle_cylinder"])
df3["vehicle_year"] = le6.transform(df3["vehicle_year"])
df3["vehicle_fuel"] = le7.transform(df3["vehicle_fuel"])
df3["vehicle_spec"] = le8.transform(df3["vehicle_spec"])

sc = MinMaxScaler()

sc.fit(df3[input_cols])
df3[input_cols] = sc.transform(df3[input_cols])

model_tree = DecisionTreeRegressor(random_state=1)
model_tree.fit(df3[input_cols], df3[target_col])
preds = model_tree.predict(df3[input_cols])
mse = mean_squared_error(df3[target_col], preds, squared=False)

mae = mean_absolute_error(df3[target_col], preds)

in_df = pd.DataFrame(
    {
        "vehicle_make":vehicle_make,
        "vehicle_model":vehicle_model,
        "vehicle_mileage":vehicle_mileage,
        "vehicle_wheel":vehicle_wheel,
        "vehicle_type":vehicle_type,
        "vehicle_cylinder":vehicle_cylinder,
        "vehicle_year":vehicle_year,
        "vehicle_fuel":vehicle_fuel,
        "vehicle_spec":vehicle_spec
    }, index=[0]
)

def single_value_prediction(df, model):
    df["vehicle_make"] = le1.transform(df["vehicle_make"])
    df["vehicle_model"] = le2.transform(df["vehicle_model"])
    df["vehicle_wheel"] = le3.transform(df["vehicle_wheel"])
    df["vehicle_type"] = le4.transform(df["vehicle_type"])
    df["vehicle_cylinder"] = le5.transform(df["vehicle_cylinder"])
    df["vehicle_year"] = le6.transform(df["vehicle_year"])
    df["vehicle_fuel"] = le7.transform(df["vehicle_fuel"])
    df["vehicle_spec"] = le8.transform(df["vehicle_spec"])
    df[input_cols] = sc.transform(df[input_cols])
    prediction = model.predict(df)
    return prediction[0]


st.markdown(f'<h5 div>Estimated Price of Above Featured Vehicle will be : <h3 div style="text-align: center;"><mark style = "background-color:#C5E8EC;color:red;font-weight:bold">AED {single_value_prediction(in_df, model_tree)}0/-</mark></div> </div>', unsafe_allow_html=True)

st.markdown(f'<h5 div>Mean Squared Error of Machine Learning Model : <h4 div style="text-align: center;"> AED {np.round(mse,2)}/-</div> </div>', unsafe_allow_html=True)
st.markdown(f'<h5 div>Mean Absolute Error of Machine Learning Model : <h4 div style="text-align: center;"> AED {np.round(mae,2)}/-</div> </div>', unsafe_allow_html=True)
