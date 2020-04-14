import pandas as pd
import plotly.graph_objs as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
from datetime import datetime

#Covid-19 Data
df_covid = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',parse_dates=['Date'])
# Merging Continent to the Covid Data
df2 = pd.read_csv('https://raw.githubusercontent.com/pdelboca/udacity-data-analysis-with-r/master/data/Countries-Continents.csv')
# Merging both Datasets to Include Continents for Covid datasets
df_main = pd.merge(df_covid,df2,how='left')
# Copy of Main DF
df = df_main.copy()

# Identify Countriens with Null Continents
null_countries= df['Continent'][df[df['Continent'].isnull()]['Country'].unique()].index
#Create a List of Continents according to identified Nulls
fill_miss_val =['Africa','Asia','Africa','Africa','Africa','Africa','Europe','Cruise Ship','Africa',
                   'Europe','Europe','Cruise Ship','Europe','Europe','Asia','Asia','North America','Asia',
                   'Africa']
# Replace Null spaces
for a,b,c in zip(null_countries,fill_miss_val,range(0,19)):
    df['Continent'][df['Country'].values == a] = fill_miss_val[c]


# Preparing Country Labels for Dropdown
country_list=[]
for country in df['Country'].unique():
    country_list.append({'label': country, 'value': country})


# Start Creation of Dash Application
app = dash.Dash()

app.layout= html.Div([

                        html.H1('Corona Display Dashboard',style={'textAlign':'center'}),
                        html.Div([html.H3('Select Country Here'),
                                    dcc.Dropdown(id='country-picker',options=country_list,value='Nigeria',
                                                multi=False)],
                                        style={'display':'inline-block','verticalAlign':'top','width':'30%'}),

                        html.Div([
                                    html.H3('Select Start Date and End Date'),
                                    dcc.DatePickerRange(id='date-picker',
                                                            min_date_allowed=datetime(2020,1,1),
                                                            max_date_allowed=datetime.today(),
                                                            start_date=datetime(2020,1,22),
                                                            end_date=datetime.today())
                                                                                ],style={'display':'inline-block'}),

                        html.Div(html.Button(id='submit-button',n_clicks=0,children='Submit',style={'fontSize':24,
                                                                                                    'marginLeft':'30px'}),
                                                                                                    style={'display':'inline-block'}),

                        html.Div(dcc.Graph(id='graph',
                                            figure={
                                                    'data':[{'x':[1,2],
                                                                'y':[3,1]}],

                                            'layout':{'title':'Please Select Country'}
                                            }))

])


@app.callback(Output('graph','figure'),[Input('submit-button','n_clicks')],
                                        [State('country-picker','value'),
                                        State('date-picker','start_date'),
                                        State('date-picker','end_date')]
                                        )
def update_graph(n_clicks,country_name,start_date,end_date):
    start_date = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end_date = datetime.strptime(end_date[:10],'%Y-%m-%d')
    #df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',parse_dates=['Date'])

    sort_df = df[df['Country']==country_name]

    # Adding the date picker Range
    date_select = pd.date_range(start_date,end_date)
    sorted_df_dates = sort_df[sort_df['Date'].isin(date_select)]


    trace0 = go.Scatter(x=sorted_df_dates['Date'],y=sorted_df_dates['Confirmed'], mode='lines+markers',name='Confirmed Cases')
    trace1 = go.Scatter(x=sorted_df_dates['Date'],y=sorted_df_dates['Recovered'], mode='lines+markers',name='Recoveries')
    trace2 = go.Scatter(x=sorted_df_dates['Date'],y=sorted_df_dates['Deaths'], mode='lines+markers',name='Deaths')

    new_fig = {'data':
                        [trace0,trace1,trace2],

                'layout':{'title':'Covid-19 Situation in {}'.format(country_name),
                                }
                }
    return new_fig



if __name__ == '__main__':
    app.run_server()
