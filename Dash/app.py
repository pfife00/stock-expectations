"""
Created on Thu Jun 20 10:22:57 2019

@author: Forest Pfeiffer
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table as dt
import pandas as pd
import base64
import configparser
import psycopg2
from dash.dependencies import Input, Output, State
import subprocess

app = dash.Dash()
#get config files from database
config = configparser.ConfigParser()
config.read('dwh.cfg')
DB_NAME = config.get('DB', 'DB_NAME')
DB_USER = config.get('DB', 'DB_USER')
DB_PASSWORD = config.get('DB', 'DB_PASSWORD')
HOST_NAME = config.get('DB', 'HOST_NAME')

#create connection to postgresql
connection = psycopg2.connect(host = HOST_NAME, port=5432, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
#cursor = connection.cursor()
valid_data = pd.read_sql_query('SELECT * FROM validation_results', connection)
orig_data = pd.read_sql_query('SELECT * FROM data_cache LIMIT 50', connection)

df=orig_data[['STOCK_TICKER', 'START_PRICE', 'MAX_PRICE', 'MIN_PRICE']]
df_valid=valid_data[['column', 'min_value', 'max_value', 'success', 'expectation_type']]
connection.commit()
connection.close()

image_filename = 'ge_round.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#pull from table and pass to df

LOGO = 'ge.jpg'
BLUE = "#1A71B7"
EDITABLE_CEL_COLOR = 'aliceblue'

#navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.Row(
            [
            html.Div(
                html.A("Great Expectations", href='https://greatexpectations.io/', target="_blank", style={"color":"white"})
                ),
            dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="100px"), width=2),
            ],
       align="center",
            ),
    ],
    brand="Stock Expectation Dash App",
    color=BLUE,
    dark=True,
)



body = dbc.Container(
    [
        dbc.Row(
            [
                # 1st column
                dbc.Col(
                    [
                        html.H2("Data"),
                        html.Div(
                        	html.Button(
                        		id = 'startButton',
                        		children = 'Start'
                        	),
                        ),
                        html.Div(
                            html.Button(
                                id = 'stopButton',
                                children = 'Stop'
                                ),
                        ),

                        html.Div(
                            id = 'startLabel'
                        ),

                        html.Div(
                            id = 'stopLabel'
                        ),
                        html.Div(
                            dcc.Interval(id='updateTable', interval=5000, n_intervals=0),
                        ),

                        html.Div(
                            dt.DataTable(
                               id = 'stockinput',
                               children = 'data',
                               row_selectable=False,
                               selected_rows=[0],
                               columns = [{'id': i, 'name': i } for i in df.columns],
                                style_table={#'overflowX': 'scroll',
                                            'maxHeight': '50'
                                            #'overflowY': 'scroll'
                                            },
                                style_data_conditional=
                                       [
                                        {
                                        'if':{'column_id':'MIN_PRICE',
                                              'filter_query':'{MIN_PRICE} < 12.00'
                                              },
                                              'backgroundColor': '#c7123f',
                                              'color': 'white',
                                        },
                                       ],
                               data= df.to_dict('records'),
                            ),
                        ),
                    ],
                    width = 5
                ),

                # 2nd column
                dbc.Col(
                    [
                        html.H2("Stock Price Expectation"),
                        html.H3("Success!"),

                        html.Div(
                            dcc.Interval(id='updateValidTable', interval=5000, n_intervals=0),
                        ),

                        dt.DataTable(
                           id = 'expectation_table',
                           columns = [{'id': i, 'name': i } for i in df_valid.columns],
                           style_table={#'overflowX': 'scroll',
                                        'maxHeight': '50',
                                        #'overflowY': 'scroll'
                                        },
                           style_data_conditional=
                                   [

                                   {
                                    'if':{'column_id':'success',
                                          'filter_query':'{success} = False'
                                          },
                                          'backgroundColor': '#ad1a1a',
                                          'color': 'white',
                                    },
                                    {
                                    'if':{'column_id':'MIN_PRICE',
                                          'filter_query':'{MIN_PRICE} < 12.00'
                                          },
                                          'backgroundColor': '#c7123f',
                                          'color': 'white',
                                    },
                                   ],
                           data= df_valid.astype(str).to_dict('records'),
                            ),
                        html.Div(
                            html.A("Great Expectations", href='https://greatexpectations.io/', target="_blank")
                            ),
                    ],
                   width = 6
                ),
            ]
        )
    ],
  #  className="mt-4",
)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([navbar,body])
# app title
app.title = "Stock Expectation"

@app.callback(
	Output('startLabel', 'children'),
	[Input('startButton','n_clicks')]
)
def startTrading(n_clicks):
	if n_clicks > 0:
		subprocess.Popen('bash run.sh', shell=True)
		return 'Started!'

@app.callback(
	Output('stopLabel', 'children'),
	[Input('stopButton', 'n_clicks')]
)
def stopTrading(n_clicks):
	if n_clicks > 0:
		subprocess.Popen('bash stop.sh', shell=True)
		return 'Stopped!'

@app.callback(
	Output('stockinput', 'data'),
	[Input('updateTable','n_intervals')]
)
def updateStockData(n):
    connection = psycopg2.connect(host = HOST_NAME, port=5432, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    orig_data = pd.read_sql_query('SELECT * FROM data_cache', connection)
    df=orig_data[['STOCK_TICKER', 'START_PRICE', 'MAX_PRICE', 'MIN_PRICE']]
    return df.to_dict('records')

@app.callback(
	Output('expectation_table', 'data'),
	[Input('updateValidTable','n_intervals')]
)
def updateStockData(n):
    connection = psycopg2.connect(host = HOST_NAME, port=5432, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    valid_data = pd.read_sql_query('SELECT * FROM validation_results', connection)
    df_valid=valid_data[['column', 'min_value', 'max_value', 'success', 'expectation_type']]
    return df_valid.astype(str).to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, host = '0.0.0.0', port=5000)
