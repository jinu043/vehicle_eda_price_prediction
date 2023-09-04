import pandas as pd
import streamlit as st

st.set_page_config(page_title="USEDCARS-ANALYSIS",
                   layout="wide", page_icon=":car:")
url = "https://www.dubicars.com/"
st.markdown('<h3 div style="text-align: center;"> <mark style = "background-color:#F3EBEC;color:darkred;font-weight:bold"> PRICE ANALYSIS OF USED CARS IN UAE</div> </div>', unsafe_allow_html=True)
st.markdown(f'<h6 div style="text-align: justify;"> When a business analyst start to do market analysis, it was really hard to collect original data from the market\
 and it was obviously time consuming and cost inefficient when we follow our usual survey method. But technological advancement has made somehow easy to have access to the real data. \
Nowdays one of the popular way to collect data from e-commerce website is by python web scrapping method. When I thought to do price analysis of used cars to boost my business analysis,  \
there is no other better method than web scrapping to collect price and other features from e-commerce website since most of the dealers publish their prices in websites. \
Now it is the time to select best e-commerce website to get price of used cars. There are many websites available or we can go to \
 dealers website directly to extract the data. Here I decided to go <a href={url}><button style="background-color:#F3EBEC;">dubicars</button></a> website to extract used cars \
 details.  </div>', unsafe_allow_html=True)
@st.cache_data
def get_data():
    data = pd.read_csv("cleaned_data.csv")
    del data["vehicle_fuel.1"]
    st.markdown('<h4 div style="text-align: center;"> LOOK AT THIS DATA!!! </div>', unsafe_allow_html=True)
    return data
data = get_data()
st.dataframe(data.head())

st.markdown(f'<h6 div style="text-align: justify;">The above table is just first five records which is already in cleaned form and there are\
 {data.shape[0]} records have collected for analysis. There were about 9800 records had been collected during web scrapping and I have further\
  reduced data by selecting vehicle model years above and equal to 2017. I have also removed some of the models and makes which does not \
  have sufficient sample records for analysis. Selected features are vehicle make, vehicle model, vehicle wheel size, vehicle mileage \
  vehicle body type, number of cylinders, model year, vehicle fuel type, vehicle specification. This above 9 features have been used for generating machine leaning \
  model for price prediction. </div>', unsafe_allow_html=True)
