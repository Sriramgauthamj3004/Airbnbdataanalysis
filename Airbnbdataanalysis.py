#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import plotly.express as px 
import streamlit as st
from streamlit_option_menu import option_menu


#Setting up page configuration

st.set_page_config(page_title="Airbnb Data visualization",
                   layout="wide")
st.sidebar.image("https://cdn.pixabay.com/animation/2023/06/13/15/13/15-13-13-522_512.gif",use_column_width=True)
def app_background():
    st.markdown(f""" <style>.stApp {{
                            background-image: url("https://freedesignfile.com/upload/2022/12/Technology-background-design-vector-illustration.jpg");
                            background-size: cover}}
                         </style>""", unsafe_allow_html=True)

app_background()


#Creating option meny in the side bar
with st.sidebar:
    selected=option_menu("Menu",["Home","Overview"],
                         icons=["house","graph-up-arrow"],
                         menu_icon="menu-button-wide")
    
#Reading the Data
df=pd.read_csv("C:/Users/Admin/Downloads/Airbnb_data.csv")
        
#Home Page
if selected=="Home":
    #Title Image
    if selected == "Home":
    # Title Image
        st.markdown("## <span style='color:blue'>Domain</span> : Travel Industry, Property Management and Tourism", unsafe_allow_html=True)
        st.markdown("## <span style='color:blue'>Technologies used</span> : Python, Pandas, Plotly, Streamlit,MongoDB",unsafe_allow_html=True)
        st.markdown("## <span style='color:blue'>Overview</span> : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.", unsafe_allow_html=True)

        st.markdown("#   ")
        st.markdown("#   ")
        

#Overview Page
if selected=="Overview":
    tab1,tab2=st.tabs(["$\huge RAW DATA $","$\huge INSIGHTS $"])

    #Raw Data Tab
    with tab1:
        if st.button("Click to Overview the dataframe"):
            st.dataframe(df)

    
    #Insights Tab
    with tab2:
        #getting user inputs
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

        #Converting user input into query
        query=f"Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}"

        #creating columns
        col1,col2=st.columns(2,gap="medium")

        with col1:
                
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df1,
                        title='Top 10 Property Types',
                        x='Listings',
                        y='Property_type',
                        orientation='h',
                        color='Property_type',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 








        #heading 1

        #creating columns
        col1,col2=st.columns(2,gap="medium")

        with col1:
            
            #avg price by room_type barchart
            pr_df=df.query(query).groupby("Room_type",as_index=False)["Price"].mean().sort_values(by="Price")
            fig=px.bar(data_frame=pr_df,
                       x="Room_type",
                       y="Price",
                       color="Price",
                       title="Avg Price in each Room type")
            st.plotly_chart(fig,use_column_width=True)

        with col2:

            #avg price in country scatter geo
            country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
            fig=px.scatter_geo(data_frame=country_df,
                               locations="Country",
                               color="Price",
                               hover_data=["Price"],
                               locationmode="country names",
                               size="Price",
                               title="Avg Price in each Country",
                               color_continuous_scale="agsunset")
            col2.plotly_chart(fig,use_column_width=True)

            # BLANK SPACE
            st.markdown("#   ")
            st.markdown("#   ")



