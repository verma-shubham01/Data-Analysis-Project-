#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


# In[3]:


from bs4 import BeautifulSoup
from numpy.core.fromnumeric import sort
import requests
import csv
from prettytable import PrettyTable
import numpy
import difflib


# In[4]:


# Position of countries dataset
df1=pd.read_csv("country_position.csv")
df1.rename(columns={'Country,Other':'Name','Latitude (generated)':'Latitude','Longitude (generated)':'Longitude'}, inplace = True)
df1.drop(df1[df1['Name']=='World'].index, inplace=True)


# Confirmed cases data for recent 30 days analysis of countries
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
confirmed = pd.read_csv(url_confirmed)
date1 = confirmed.columns[4:]
covid_data1= confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
covid_data1['date'] = pd.to_datetime(covid_data1['date'])
data2 = covid_data1.groupby(['date', 'Country/Region'])[['confirmed']].sum().reset_index()

#Vaccination data
df_vaccination = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
df_vaccination.rename(columns={"location":"Name"},inplace=True)
r={'Cape Verde':'Cabo Verde','Central African Republic':'CAR',"Cote d'Ivoire":"Ivory Coast",'Curacao':'Curaçao','Democratic Republic of Congo':'Congo','Northern Cyprus':'Cyprus','Northern Ireland':'Ireland',
'Saint Vincent and the Grenadines':'St. Vincent Grenadines','Sint Maarten (Dutch part)':'Saint Martin','South Korea':'S. Korea','Turks and Caicos Islands':'Turks and Caicos',
'United Arab Emirates':'UAE','United Kingdom':'UK','United States':'USA'}
df_vaccination['Name']=df_vaccination['Name'].replace(r)
df_vaccination=df_vaccination[['Name','total_vaccinations','people_vaccinated','people_fully_vaccinated','total_boosters']]


# In[5]:


# Web scrape data for update data every day
#first dataset
field_list = ["Name","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","New Recovered","Active Cases","Serious Cases","Total Tests","Population"]
url = requests.get("https://www.worldometers.info/coronavirus/").text
soup = BeautifulSoup(url,"lxml")

table1=soup.find('table',id="main_table_countries_yesterday")
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)
headers[13] = 'Tests/1M pop'
mydata = pd.DataFrame(columns = headers)
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row
mydata.drop(mydata.index[0:7], inplace=True)
mydata.drop(mydata.index[222:229], inplace=True)
mydata.reset_index(inplace=True, drop=True)
mydata.to_csv('covid_data.csv', index=False) 

# second dataset
table2=soup.find('table',id="main_table_countries_yesterday2")
headers = []
for i in table2.find_all('th'):
    title = i.text
    headers.append(title)
headers[13] = 'Tests/1M pop'
mydata3 = pd.DataFrame(columns = headers)
for j in table2.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata3)
    mydata3.loc[length] = row
mydata3.drop(mydata3.index[0:7], inplace=True)
mydata3.drop(mydata3.index[222:229], inplace=True)
mydata3.reset_index(inplace=True, drop=True)
mydata3.to_csv('covid_data2.csv', index=False)


# In[6]:


pd.options.mode.chained_assignment = None
# data manipulation

# for first dataset
mydata2 = pd.read_csv('covid_data.csv')
df=mydata2[['Country,Other','TotalRecovered','NewRecovered','ActiveCases','TotalTests','TotalCases','NewCases','TotalDeaths','NewDeaths','Population']]
df.at[2,'Population']='335,231,650'
df.drop_duplicates(inplace=True)
df.sort_values(["Country,Other"],inplace=True)
df.drop(df.loc[df['Country,Other'] =="World"].index, inplace = True)
df.drop(df.loc[df['Country,Other'] =="Total:"].index, inplace = True)

df['NewDeaths'] = df['NewDeaths'].astype(str)

df['NewCases'] = df['NewCases'].str.replace('+', '')
df['NewDeaths'] = df['NewDeaths'].str.replace('+', '')
df['NewRecovered'] = df['NewRecovered'].str.replace('+', '')

cols=['TotalCases','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases',"TotalTests","Population"]
df[cols] = df[cols].replace({'\$': '', ',': ''," ":'',"nan":"NaN","N/A":"NaN"}, regex=True)
df['NewDeaths'] = df['NewDeaths'].astype(float)
df.fillna(0, inplace=True)

df[['TotalCases','TotalTests','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases','Population']] = df[['TotalCases','TotalTests','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases','Population']].apply(pd.to_numeric)

# for second dataset
mydata4 = pd.read_csv('covid_data2.csv')
ydf=mydata4[['Country,Other','TotalRecovered','NewRecovered','ActiveCases','TotalTests','TotalCases','NewCases','TotalDeaths','NewDeaths']]
ydf.drop_duplicates(inplace=True)
ydf.sort_values(["Country,Other"],inplace=True)
ydf.drop(ydf.loc[ydf['Country,Other'] =="World"].index, inplace = True)
ydf.drop(ydf.loc[ydf['Country,Other'] =="Total:"].index, inplace = True)

ydf['NewDeaths'] = ydf['NewDeaths'].astype(str)

ydf['NewCases'] = ydf['NewCases'].str.replace('+', '')
ydf['NewDeaths'] = ydf['NewDeaths'].str.replace('+', '')
ydf['NewRecovered'] = ydf['NewRecovered'].str.replace('+', '')

cols1=['TotalCases','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases',"TotalTests"]
ydf[cols1] = ydf[cols1].replace({'\$': '', ',': ''," ":'',"nan":"NaN","N/A":"NaN"}, regex=True)
ydf['NewDeaths'] = ydf['NewDeaths'].astype(float)

ydf.fillna(0, inplace=True)

ydf[['TotalCases','TotalTests','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases']] = ydf[['TotalCases','TotalTests','NewCases','TotalDeaths','NewDeaths','TotalRecovered','NewRecovered','ActiveCases']].apply(pd.to_numeric)
ydf.rename(columns = {'Country,Other':'Name'}, inplace = True)

# Import date 
from datetime import date 
from datetime import timedelta
yesterday=(date.today()-timedelta(days = 1))
df['date'] = pd.Timestamp(yesterday)
df.rename(columns = {'Country,Other':'Name'}, inplace = True)
df = df[['date','Name','TotalRecovered','NewRecovered','ActiveCases','TotalTests','TotalCases','NewCases','TotalDeaths','NewDeaths','Population']]


# In[7]:


# merge dataset
df = df.merge(right=df1, how='inner')

# create dictionary of list
covid_data_dict = df[['Name', 'Latitude', 'Longitude']]
list_locations = covid_data_dict.set_index('Name')[['Latitude', 'Longitude']].T.to_dict('dict')


# In[8]:


# web app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo1.jpg'),
                     id='corona-image',
                     style={
                         "height": "60px",
                         "width": "auto",
                         "margin-bottom": "25px",
                     },
                     )
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H3("COVID-19", style={"margin-bottom": "0px", 'color': 'red',"font-weight": "bold"}),
                html.H5("Keep in sight Covid - 19 Cases", style={"margin-top": "0px", 'color': 'magenta'}),
                html.H3("Stay home, stay safe", style={"margin-top": "0px", 'color': 'green'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.H6('Last Updated: ' + str(df['date'].iloc[-1].strftime("%B %d, %Y")) + '  00:01 (UTC)',
                    style={'color': 'orange'}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.H6(children='Global Cases',
                    style={
                        'textAlign': 'center',
                        'color': 'dark'}
                    ),

            html.P(f"{df['TotalCases'].sum():,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{df['NewCases'].sum():,.0f} "
                   + ' (' + str(round(((df["NewCases"].sum()) /
                                      df["TotalCases"].sum())* 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Global Deaths',
                    style={
                        'textAlign': 'center',
                        'color': 'dark'}
                    ),

            html.P(f"{df['TotalDeaths'].sum():,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{df['NewDeaths'].sum():,.0f} "
                   + ' (' + str(round(((df["NewDeaths"].sum()) /
                                       df["TotalDeaths"].sum()) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Global Recovered',
                    style={
                        'textAlign': 'center',
                        'color': 'dark'}
                    ),

            html.P(f"{df['TotalRecovered'].sum():,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40}
                   ),
                 
            html.P('new:  ' + f"{df['NewRecovered'].sum():,.0f} "
                   + ' (' + str(round(((df["NewRecovered"].sum()) /
                                       df["TotalRecovered"].sum()) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns",
        ),

        html.Div([
            html.H6(children='Global Active',
                    style={
                        'textAlign': 'center',
                        'color': 'dark'}
                    ),

            html.P(f"{df['ActiveCases'].sum():,.0f}",
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 40}
                   ),

            html.P('new:  ' + f"{((df['NewCases'].sum())-(df['NewDeaths'].sum()))-(df['NewRecovered'].sum()):,.0f} "
                   + ' (' + str(round(((((df['NewCases'].sum())-(df['NewDeaths'].sum()))-(df['NewRecovered'].sum())) /
                                       df['ActiveCases'].sum()) * 100, 2)) + '%)',
                   style={
                       'textAlign': 'center',
                       'color': '#e55467',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], className="card_container three columns")

    ], className="row flex-display"),

    html.Div([
        html.Div([

                    html.P('Select Country:', className='fix_label',  style={'color': 'white'}),

                     dcc.Dropdown(id='w_countries',
                                  multi=False,
                                  clearable=True,
                                  value='India',
                                  placeholder='Select Countries',
                                  options=[{'label': c, 'value': c}
                                           for c in (df['Name'].unique())], className='dcc_compon'),

                     html.P('New Cases : ' + '  ' + ' ' + str(df['date'].iloc[-1].strftime("%B %d, %Y")) + '  ', className='fix_label',  style={'color': 'white', 'text-align': 'center'}),
                     dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '20px'},
                     ),

                      dcc.Graph(id='death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='recovered', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

                      dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                      ),

        ], className="create_container three columns", id="cross-filter-options"),
            html.Div([
                      dcc.Graph(id='pie_chart',
                              config={'displayModeBar': 'hover'}),
                              ], className="create_container four columns"),

                    html.Div([
                        dcc.Graph(id="line_chart")

                    ], className="create_container five columns"),

        ], className="row flex-display"),
    
    
html.Div([
    html.Div([
            html.H6(children='Total Vaccination Doses',
                    style={'font-size':22,
                        'textAlign': 'center',
                        'color': 'darkgreen',"font-weight": "bold"}
                    ),
        dcc.Graph(id='dose', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '-10px'},
                     )
], className="card_container three columns",
        ),
    html.Div([
            html.H6(children='Total Vaccinated People',
                    style={'font-size':22,
                        'textAlign': 'center',
                        'color': 'darkgreen',"font-weight": "bold"}
                    ),
        dcc.Graph(id='vacpeople', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '-10px','margin-left': '-20px','margin-right': '-20px'},
                     )
], className="card_container three columns",
        ),
    html.Div([
            html.H6(children='Total Fully Vaccinated',
                    style={'font-size':22,
                        'textAlign': 'center',
                        'color': 'darkgreen',"font-weight": "bold"}
                    ),
        dcc.Graph(id='fullvac', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '-10px','margin-left': '-20px','margin-right': '-20px'},
                     )
], className="card_container three columns",
        ),
    html.Div([
            html.H6(children='Total Boosted People',
                    style={'font-size':22,
                        'textAlign': 'center',
                        'color': 'darkgreen',"font-weight": "bold"}
                    ),
        dcc.Graph(id='totalboost', config={'displayModeBar': False}, className='dcc_compon',
                     style={'margin-top': '-10px','margin-left': '-20px','margin-right': '-20px'},
                     )
], className="card_container three columns",
        ),
    ], className="row flex-display"),    



html.Div([
        html.Div([
            dcc.Graph(id="map")], className="create_container1 twelve columns"),

            ], className="row flex-display"),

    ], id="mainContainer",
    style={"display": "flex", "flex-direction": "column"})


@app.callback(
    Output('dose','figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    value_vac = df_vaccination[df_vaccination['Name'] == w_countries]['total_vaccinations'].iloc[-1]
    
    return {
            'data': [go.Indicator(
                    mode='number',
                    value=value_vac,
                    
                    number={'valueformat': ',',
                            'font': {'size': 25},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
    'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#0723ee'),
                paper_bgcolor='#DCDCDC',
                plot_bgcolor='#1f2c56',
                height=70
                )}

@app.callback(
    Output('vacpeople','figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    value_vacpeople = df_vaccination[df_vaccination['Name'] == w_countries]['people_vaccinated'].iloc[-1]
    percent_vacpeople=round((df_vaccination[df_vaccination['Name'] == w_countries]['people_vaccinated'].iloc[-1]/df[df['Name'] == w_countries]['Population'].iloc[0])*100,2)
    return {
            'data': [go.Indicator(
                    mode='number',
                    value=value_vacpeople,
                    
                    number={'valueformat': ',',
                            'font': {'size': 25},

                               },
                    domain={'y': [0,1], 'x': [0,.4]}),
                    
                     go.Indicator(
                    mode='number',
                    value=percent_vacpeople,
                    
                    number={'valueformat': '.','prefix': "        (",'suffix':"%)",
                            'font': {'size': 15,'color':'#b300b3'},

                               },
                    domain={'y': [0, 1], 'x': [0.9999,1]})],
    'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#0723ee'),
                paper_bgcolor='#DCDCDC',
                plot_bgcolor='#1f2c56',
                height=70
                )}


@app.callback(
    Output('fullvac','figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    value_vac = df_vaccination[df_vaccination['Name'] == w_countries]['people_fully_vaccinated'].iloc[-1]
    percent_vac=round((df_vaccination[df_vaccination['Name'] == w_countries]['people_fully_vaccinated'].iloc[-1]/df[df['Name'] == w_countries]['Population'].iloc[0])*100,2)
    return {
            'data': [go.Indicator(
                    mode='number',
                    value=value_vac,
                    
                    number={'valueformat': ',',
                            'font': {'size': 25},

                               },
                    domain={'y': [0,1], 'x': [0,.4]}),
                    
                     go.Indicator(
                    mode='number',
                    value=percent_vac,
                    
                    number={'valueformat': '.','prefix': "        (",'suffix':"%)",
                            'font': {'size': 15,'color':'#b300b3'},

                               },
                    domain={'y': [0, 1], 'x': [0.9999,1]})],
    'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#0723ee'),
                paper_bgcolor='#DCDCDC',
                plot_bgcolor='#1f2c56',
                height=70
                )}

@app.callback(
    Output('totalboost','figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    boost_vac = df_vaccination[df_vaccination['Name'] == w_countries]['total_boosters'].iloc[-1]
    percent_boost=round((df_vaccination[df_vaccination['Name'] == w_countries]['total_boosters'].iloc[-1]/df[df['Name'] == w_countries]['Population'].iloc[0])*100,2)
    return {
            'data': [go.Indicator(
                    mode='number',
                    value=boost_vac,
                    
                    
                    number={'valueformat': ',',
                            'font': {'size': 25},

                               },
                    domain={'y': [0, 1], 'x': [0, .4]}),
                    go.Indicator(
                    mode='number',
                    value=percent_boost,
                    
                    number={'valueformat': '.','prefix': "        (",'suffix':"%)",
                            'font': {'size': 15,'color':'#b300b3'},

                               },
                    domain={'y': [0, 1], 'x': [.9999, 1]})],
    'layout': go.Layout(
                title={
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#0723ee'),
                paper_bgcolor='#DCDCDC',
                plot_bgcolor='#1f2c56',
                height=70
                )}

@app.callback(
    Output('confirmed', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    
    value_confirmed = df[df['Name'] == w_countries]['NewCases'].iloc[0]
    delta_confirmed = ydf[ydf['Name'] == w_countries]['NewCases'].iloc[0]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_confirmed,
                    delta={'reference': delta_confirmed,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Confirmed',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='orange'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }
@app.callback(
    Output('death', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    
    value_death = df[df['Name'] == w_countries]['NewDeaths'].iloc[0]
    delta_death = ydf[ydf['Name'] == w_countries]['NewDeaths'].iloc[0]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_death,
                    delta={'reference': delta_death,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Death',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#dd1e35'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

@app.callback(
    Output('recovered', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
   
    value_recovered = df[df['Name'] == w_countries]['NewRecovered'].iloc[0]
    delta_recovered = ydf[ydf['Name'] == w_countries]['NewRecovered'].iloc[0]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_recovered,
                    delta={'reference': delta_recovered,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Recovered',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='green'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

@app.callback(
    Output('active', 'figure'),
    [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    
    value_active = df[df['Name'] == w_countries]['NewCases'].iloc[0]
    delta_active = ydf[ydf['Name'] == w_countries]['NewCases'].iloc[0]
    return {
            'data': [go.Indicator(
                    mode='number+delta',
                    value=value_active,
                    delta={'reference': delta_active,
                              'position': 'right',
                              'valueformat': ',g',
                              'relative': False,

                              'font': {'size': 15}},
                    number={'valueformat': ',',
                            'font': {'size': 20},

                               },
                    domain={'y': [0, 1], 'x': [0, 1]})],
            'layout': go.Layout(
                title={'text': 'New Active',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'},
                font=dict(color='#e55467'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50
                ),

            }

# pie chart (total casualties in country)
@app.callback(Output('pie_chart', 'figure'),
              [Input('w_countries', 'value')])

def update_graph(w_countries):
    new_confirmed = df[df['Name'] == w_countries]['TotalCases'].iloc[0]
    new_death = df[df['Name'] == w_countries]['TotalDeaths'].iloc[0]
    new_recovered = df[df['Name'] == w_countries]['TotalRecovered'].iloc[0]
    new_active = df[df['Name'] == w_countries]['ActiveCases'].iloc[0]
    colors = ['orange', '#dd1e35', 'green', '#e55467']

    return {
        'data': [go.Pie(labels=['Confirmed', 'Death', 'Recovered', 'Active'],
                        values=[new_confirmed, new_death, new_recovered, new_active],
                        marker=dict(colors=colors),
                        hoverinfo='label+value+percent',
                        textinfo='label+value',
                        textfont=dict(size=13),
                        hole=.7,
                        rotation=45
                       


                        )],

        'layout': go.Layout(
            
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': 'Total Cases : ' + (w_countries),


                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
            ),


        }

# bar chart (recent 30 days' new cases)
@app.callback(Output('line_chart', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
# main data frame
    data2 = covid_data1.groupby(['date', 'Country/Region'])[['confirmed']].sum().reset_index()
    data2["Country/Region"]=data2["Country/Region"].replace({"US":"USA","United Kingdom":"UK","United Arab Emirates":"UAE","Taiwan*":"Taiwan","Saint Vincent and the Grenadines":"St. Vincent Grenadines"})
# daily confirmed
    covid_data_3 = data2[data2['Country/Region'] == w_countries][['Country/Region', 'date', 'confirmed']].reset_index()
    
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()

    return {
        'data': [go.Bar(x=covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30),
                        y=covid_data_3[covid_data_3['Country/Region'] == w_countries]['daily confirmed'].tail(30),

                        name='Daily confirmed',
                        marker=dict(
                            color='orange'),
                        hoverinfo='text',
                        hovertext=
                        '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30).astype(str) + '<br>' +
                        '<b>Daily confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == w_countries]['daily confirmed'].tail(30)] + '<br>' +
                        '<b>Country</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['Country/Region'].tail(30).astype(str) + '<br>'


                        ),
                 go.Scatter(x=covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30),
                            y=covid_data_3[covid_data_3['Country/Region'] == w_countries]['Rolling Ave.'].tail(30),
                            mode='lines',
                            name='Rolling average of the last seven days - daily confirmed cases',
                            line=dict(width=3, color='#FF00FF'),
                            
                            hoverinfo='text',
                            hovertext=
                            '<b>Date</b>: ' + covid_data_3[covid_data_3['Country/Region'] == w_countries]['date'].tail(30).astype(str) + '<br>' +
                            '<b>Rolling Ave.(last 7 days)</b>: ' + [f'{x:,.0f}' for x in covid_data_3[covid_data_3['Country/Region'] == w_countries]['Rolling Ave.'].tail(30)] + '<br>'
                            )],


        'layout': go.Layout(
             plot_bgcolor='#1f2c56',
             paper_bgcolor='#1f2c56',
             title={
                'text': 'Last 30 Days Confirmed Cases : ' + (w_countries),
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'white',
                        'size': 20},

             hovermode='x',
             margin = dict(r = 0),
             xaxis=dict(title='<b>Date</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='white'
                        )

                ),

             yaxis=dict(title='<b>Daily confirmed Cases</b>',
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                           family='Arial',
                           size=12,
                           color='white'
                        )

                ),

            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.3},
                          font=dict(
                              family="sans-serif",
                              size=12,
                              color='white'),

                 )

    }



# scattermapbox chart (analysis on world map)
@app.callback(Output('map', 'figure'),
              [Input('w_countries', 'value')])
def update_graph(w_countries):
    covid_data_1 = df
    covid_data_2 = covid_data_1[covid_data_1['Name'] == w_countries]

    if w_countries:
        zoom = 2
        zoom_lat = list_locations[w_countries]['Latitude']
        zoom_lon = list_locations[w_countries]['Longitude']

    return {
        'data': [go.Scattermapbox(
                         lon=covid_data_2['Longitude'],
                         lat=covid_data_2['Latitude'],
                         mode='markers',
                         marker=go.scattermapbox.Marker(
                                  size=covid_data_2['TotalCases'] / 1500,
                                  color=covid_data_2['TotalCases'],
                                  colorscale='hsv',
                                  showscale=False,
                                  sizemode='area',
                                  opacity=0.3),

                         hoverinfo='text',
                         hovertext=
                         '<b>Country</b>: ' + covid_data_2['Name'].astype(str) + '<br>' +
                         '<b>Longitude</b>: ' + covid_data_2['Longitude'].astype(str) + '<br>' +
                         '<b>Latitude</b>: ' + covid_data_2['Latitude'].astype(str) + '<br>' +
                         '<b>Confirmed</b>: ' + [f'{x:,.0f}' for x in covid_data_2['TotalCases']] + '<br>' +
                         '<b>Death</b>: ' + [f'{x:,.0f}' for x in covid_data_2['TotalDeaths']] + '<br>' +
                         '<b>Recovered</b>: ' + [f'{x:,.0f}' for x in covid_data_2['TotalRecovered']] + '<br>' +
                         '<b>Active</b>: ' + [f'{x:,.0f}' for x in covid_data_2['ActiveCases']] + '<br>'

                        )],


        'layout': go.Layout(
             margin={"r": 0, "t": 0, "l": 0, "b": 0},
             
             hovermode='closest',
             mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center=go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_lon),
                
                style='dark',
                zoom=zoom
             ),
             autosize=True,

        )

    }

if __name__ == '__main__':
    
    app.run()


# In[ ]:





# In[ ]:




