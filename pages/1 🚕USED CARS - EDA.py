import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_icon=":car:")

@st.cache_data
def get_data():
    data = pd.read_csv("ml_data.csv")
    return data
data = get_data()

st.markdown('<h2 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:darkred;font-weight:bold">EXPLORATORY DATA ANALYSIS - UAE USED CARS FROM DUBICARS WEBSITE</mark></div>', unsafe_allow_html=True)

st.divider()

@st.cache_data
def get_data_df1():
    df = pd.DataFrame(data["vehicle_make"].value_counts()).reset_index().rename(columns={"index":"vehicle_make",
                                                                                      "vehicle_make":"count"})
    return df
df1 = get_data_df1()
def top_makes_dist(df, n):
    fig = px.bar(df1.head(n), x="vehicle_make", y="count", color_discrete_sequence =['red']*len(df),
                 title= f"Distribution of top {n} vehicle makes", height=400)
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"))
    fig.update_xaxes(
        tickangle=30,
        title_font={"size": 20, "color":"black"},
        title_standoff=15)
    fig.update_yaxes(
        tickangle=0,
        title_font={"size": 20, "color":"black"},
        title_standoff=15)
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title = {
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
    🚘Which makes have most number of vehicles</mark></div>', unsafe_allow_html=True)
    n1 = st.number_input(f"Top Makes", 8, len(df1), step=1)
    st.plotly_chart(top_makes_dist(df1, n=n1), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
    We can see that Benz is having highest number of makes as per last month data and followed by Nissan, Toyota, Ford etc</mark></div>', unsafe_allow_html=True)

makes = []
models = []
count = []
for make in data["vehicle_make"].unique():
    dfme = data.query(f'vehicle_make == "{make}"')
    for model in dfme["vehicle_model"].unique():
        dfml = data.query(f'vehicle_model == "{model}"')
        makes.append(make)
        models.append(model)
        count.append(len(dfml))

df2 = pd.DataFrame(
{
    "make":makes,
    "model":models,
    "count":count
})

def top_models_dist(df, n, make):
    dfm = df[df["make"]==f"{make}"].sort_values(by="count", ascending=False).head(n)
    dfm["model"] = dfm["model"].astype(object)
    fig = px.bar(dfm, x="model", y="count", title=f'Models distribution of vehicle make {make}',
                color_discrete_sequence =['green']*len(df), color_continuous_scale=['green']*len(df), height=400)
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"))
    fig.update_xaxes(
        tickangle=30,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_yaxes(
        tickangle=0,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(xaxis_type='category')
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig

with col2:
    st.markdown(f'<h6 div style="text-align: center;color:#cc6600;font-weight:bold;font-family:verdana">\
        🚔From each make who have most vehicles</mark></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        make = st.selectbox("Vehicle Make", df2["make"].unique().tolist(), index=3)
    with c2:
        n2 = st.number_input(f"Top Models", 8, len(df1), step=1)

    st.plotly_chart(top_models_dist(df2, n=n2, make=make), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
    When you change the makes, you will get distribution of each model from the respective make. For example, when you select Toyota, you can see that corolla and Rav4 have most\
    number of vehicles followed by Yaris, Camry etc. </mark></div>', unsafe_allow_html=True)

st.divider()

col3, col4 = st.columns(2)

makes = []
vehicle_type = []
count = []
for make in data["vehicle_make"].unique():
    dfme = data.query(f'vehicle_make == "{make}"')
    for type_ in dfme["vehicle_type"].unique():
        dfvt = dfme.query(f'vehicle_type == "{type_}"')
        makes.append(make)
        vehicle_type.append(type_)
        count.append(len(dfvt))

df3 = pd.DataFrame(
{
    "make":makes,
    "vehicle_type":vehicle_type,
    "count":count
})

def vehicle_type_prop(df, make):
    df_ = df.query(f'make == "{make}"')
    fig = px.pie(df_, values="count", names="vehicle_type", hole=0.1, title = f'Proportion of {make} by vehicle types')
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"), textinfo='percent+label')
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title={
        'y': 0.95,
        'x': 0.4,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig
with col3:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
            🚍Is My Body Type Highest in Proportion</mark></div>', unsafe_allow_html=True)
    make = st.selectbox("Vehicle Make", df3["make"].unique().tolist())
    st.plotly_chart(vehicle_type_prop(df3, make), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
    When you change the make, you can get vehicles distribution in different body types. For example lets take toyota make, SUV type of vehicles\
    in highest proportion followed by sedan. Similarly you can see other makes proportions as well.</mark></div>', unsafe_allow_html=True)


makes = []
models = []
years = []
count = []

for make in data["vehicle_make"].unique():
    dfme = data.query(f'vehicle_make == "{make}"')
    for model in dfme["vehicle_model"].unique():
        dfml = dfme.query(f'vehicle_model == "{model}"')
        for year in dfml["vehicle_year"].unique():
            dfvy = dfml.query(f'vehicle_year == {year}')
            makes.append(make)
            models.append(model)
            years.append(year)
            count.append(len(dfvy))

@st.cache_data
def get_df4():
    df = pd.DataFrame(
    {
        "make":makes,
        "model":models,
        "year":years,
        "count":count
    })
    return df
df4 = get_df4()

def vehicle_year_prop(df, make, model):
    df_ = df.query(f'make == "{make}" and model == "{model}"')
    fig = px.pie(df_, values="count", names="year", hole=0.1, title = f'Proportion of {make} by vehicle years')
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"), textinfo='percent+label')
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title={
        'y': 0.95,
        'x': 0.4,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig

with col4:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
                📅Does my model year dominated more</mark></div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        make = st.selectbox("vehicle Make", df4['make'].unique().tolist())
    with c4:
        model = st.selectbox("vehicle Model", df4.query(f'make == "{make}"')["model"].unique().tolist())
    st.plotly_chart(vehicle_year_prop(df4, make, model), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
        When you change the make and model, you could get distribution of vehicles by model years. Lets select Hyundai Accent, you can see that\
        2020 model dominated in more followed by model 2019 model. Similarly you can get other models distribution as well. </mark></div>',
                unsafe_allow_html=True)

st.divider()

dealers = []
vehicle_total = []
for dealer in data["vehicle_dealer"].unique():
    df = data.query(f'vehicle_dealer == "{dealer}"')
    dealers.append(dealer)
    vehicle_total.append(len(df))

dealers_vehicles = pd.DataFrame(
{
    "dealer":dealers,
    "vehicle_total":vehicle_total
}).sort_values(by="vehicle_total", ascending=False)

def vehicles_by_dealers(n):
    df = dealers_vehicles.query('dealer != "Private Seller"').head(n)
    fig = px.bar(df, x="dealer", y="vehicle_total", title=f"Vehicles Distribution by top {n} dealers",
                color_discrete_sequence =['magenta']*len(df), height=500)
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"))
    fig.update_xaxes(
        tickangle=30,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_yaxes(
        tickangle=0,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig
col5, col6 = st.columns(2)
with col5:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
                    🎢 As a delaer am I having more vehicles</mark></div>', unsafe_allow_html=True)
    n = st.number_input("TOP DEALERS", 5, len(dealers_vehicles))
    st.plotly_chart(vehicles_by_dealers(n=n), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
        From the above plot, you can see that cars24 is having highest vehicles in hand followed by Linda cars, Wadishee used cars etc.</mark></div>',unsafe_allow_html=True)

makes = []
dealers = []
count = []

for make in data["vehicle_make"].unique():
    dfme = data.query(f'vehicle_make == "{make}"')
    for dealer in dfme["vehicle_dealer"].unique():
        dfvy = dfme.query(f'vehicle_dealer == "{dealer}"')
        makes.append(make)
        dealers.append(dealer)
        count.append(len(dfvy))

df5 = pd.DataFrame(
{
    "make":makes,
    "dealer":dealers,
    "count":count
})

def vehicle_dealers_prop(df, make, n):
    df_ = df.query(f'make == "{make}" and dealer != "Private Seller"').sort_values(by="count", ascending=False).head(n)
    fig = px.pie(df_, values="count", names="dealer", hole=0.1, title = f'Proportion of vehicle {make} in hand by top {n} dealers', height=500)
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"), textinfo='percent')
    fig.update_xaxes(
        tickangle=30,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_yaxes(
        tickangle=0,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title=dict(font=dict(size=20)))
    return fig
with col6:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
                        🤝Is my model more in market</mark></div>', unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        make = st.selectbox("Make", df5["make"].unique().tolist())
    with c4:
        n = st.number_input("Top Dealers", 5, step=1)
    st.plotly_chart(vehicle_dealers_prop(df5, make, n), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
    When you change the make, you can see the vehicles distribution by top dealers. As an example, when you select nissan you can see that cars24\
    delaer have most number of cars followed by swaiden motors, vesla motors etc.</mark></div>', unsafe_allow_html=True)

st.divider()

col7, col8 = st.columns(2)
def price_distribution(df, make, model, year):
    df_ = df.query(f'vehicle_make == "{make}" and vehicle_model =="{model}" and vehicle_year == {year}')
    df_ = df_.query('vehicle_price != "Ask for price"').copy()
    df_["vehicle_price"] = df_["vehicle_price"].astype(int)
    fig = px.histogram(df_, x="vehicle_price", title=f'Price Distribution - {make}-{model}-{year}',
                      color_discrete_sequence =['orange']*len(df))
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=16,
        font_family="Rockwell"))
    fig.update_xaxes(
        tickangle=30,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_yaxes(
        tickangle=0,
        title_font={"size": 20, "color": "black"},
        title_standoff=15)
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(bargap=0.05)
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig

with col7:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
                            💸Would you like to see my price range</mark></div>', unsafe_allow_html=True)
    c5, c6, c7 = st.columns(3)
    with c5:
        make = st.selectbox("Vehicle Brand", data["vehicle_make"].unique().tolist())
    with c6:
        model = st.selectbox("Vehicle Model", data.query(f'vehicle_make == "{make}"')["vehicle_model"].unique().tolist())
    with c7:
        year = st.selectbox("Vehicle_Year", data.query(f'vehicle_make == "{make}" and vehicle_model =="{model}"')["vehicle_year"].unique().tolist())
    st.plotly_chart(price_distribution(data, make, model, year), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
        From the above histogram plot, you can see the distribution of different models price distribution. Lets select Kia Optima 2020 model, you can see that\
        price range would be between AED 20k - AED 80k. Please note price of vehicles depends on mileage as well as vehicle dealer. </mark></div>',unsafe_allow_html=True)

def mileage_vs_price(df, make, model, year):
    df_ = df.query(f'vehicle_make == "{make}" and vehicle_model =="{model}" and vehicle_year == {year}')
    df_ = df_.query('vehicle_price != "Ask for price"').copy()
    df_["vehicle_price"] = df_["vehicle_price"].astype(int)
    fig = px.scatter(df_, x="vehicle_mileage", y="vehicle_price", color="vehicle_dealer", title = f'Vehicle Price Vs Vehicle Mileage - {make}-{model}-{year}')
    fig.update_traces(hoverlabel = dict(font=dict(color='black'), bgcolor="white",
        font_size=18,
        font_family="Rockwell"), marker=dict(size=15,
                                             line=dict(width=1)))
    fig.update_xaxes(
        tickangle=0,
        title_font={"size": 20, "color": "black"},
        title_standoff=15, showgrid=True, showline=True, gridcolor="lightblue")
    fig.update_yaxes(
        tickangle=0,
        title_font={"size": 20, "color": "black"},
        title_standoff=15, showgrid=True, showline=True, gridcolor="lightblue")
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title=dict(font=dict(size=20)))
    fig.update_layout(title={
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })
    return fig
with col8:
    st.markdown(f'<h6 div style="text-align: center;"><mark style = "background-color:#F3EBEC;color:#cc6600;font-weight:bold;font-family:verdana">\
                                🛣️Does mileage really effecting vehicles price</mark></div>', unsafe_allow_html=True)
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.markdown("<div></div>", unsafe_allow_html=True)
    st.plotly_chart(mileage_vs_price(data, make, model, year), use_container_width=True)
    st.markdown(f'<h6 div style="text-align: justify;"><mark style = "background-color:#F3EBEC;color:#993366;font-weight:bold;font-family:verdana">\
        We expected inverse proportion of vehicles price with mileage, but it is not. Price of vehicles is depending vehicle dealer as well.\
        We are not getting linear relationship between vehicle price and mileage. Therefore these features (mileage and dealer) would effect our \
        machine learning model for price prediction.</mark></div>',unsafe_allow_html=True)
