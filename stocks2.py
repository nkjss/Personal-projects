import yfinance as yf
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash import Dash, dash_table
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


class stock_comp:
    def __init__(self,icon,past):
        
        self.icon = icon

        if past:
            self.past = int(past)
        else:
            self.past = 0

        #self.past = past
        
        company = yf.Ticker(icon)
        company_data = company.history(period="max")

        company_data.reset_index(inplace = True)

        df_company = company_data.tail(self.past)

        df_company.drop(['Open','High','Low','Volume','Stock Splits','Dividends'], axis = 1, inplace = True)

        df_company.rename(columns = {'Close':icon}, inplace = True)

        self.df_company = df_company

    



app = Dash(external_stylesheets=[dbc.themes.SLATE])


app.layout = html.Div(
    children=[
    html.H1('Stocks comparison(Closing price)', style={'textAlign': 'center', 'color': '#FFD700', 'font-size': 30}),

    html.Br(),

    html.Div([
        html.P('Stock 1:', style = {'font-size':20,'margin-left': 60, 'margin-right': 5,'margin-top':9, 'color':'blue'}),
        html.Div(dcc.Input(id = 'input-s1', placeholder='Enter a stock ticker.',type='text',value='aapl',style = {'width':700, 'height':35}))
        ],style={'display':'flex', 'flex-direction':'row' ,'align-items':'center'}),

    html.Div([
        html.P('Stock 2:', style = {'font-size':20, 'margin-left': 60 ,'margin-right': 5, 'margin-top':9, 'color':'red'}),
        html.Div(dcc.Input(id = 'input-s2', placeholder='Enter a stock ticker.',type='text',value='GOOGL',style = {'width':700, 'height': 35, 'margin-right': 50})),
        html.P('History:', style = {'font-size':20, 'margin-right': 5, 'margin-top': 9}),
        html.Div(dcc.Input(id = 'input-past',placeholder='Enter history (days ago)',type='text',value='',style = {'width':170, 'height': 35}))
        ],style={'display':'flex', 'flex-direction':'row' ,'align-items':'center'}),

    html.Div([
    
    html.Div([
    
    html.Div( dbc.Card( dbc.CardBody(html.Div([], id='plot1') )),style = {'margin-bottom':10} ),
    html.H5('Correlation Matrix', style = {'margin-left':20, 'color':'white'}),
    html.Div( dbc.Card([ dbc.CardBody(dash_table.DataTable(id = 'corr', style_table={'color':'black'} ))] )),

    ]),

    html.Div([
    
    html.Div( dbc.Card([ dbc.CardBody(dash_table.DataTable(id = 'df', style_table={'overflowX': 'scroll', 'height': '600px', 'color':'black'} ))] ),  )
    ]),

     

    ], style = { 'display': 'grid', 'grid-template-columns': '2.5fr 1.5fr' } ),

  
    
    

    ]
)






@app.callback(
        [Output(component_id='plot1', component_property='children'),
         Output(component_id='corr', component_property='data'),
         Output(component_id='df', component_property='data'),],
           

        [Input(component_id='input-s1', component_property='value'),
         Input(component_id='input-s2', component_property='value'),
         Input(component_id='input-past', component_property='value')],
        
        [State("plot1", 'children'),State("corr", 'children'),State("df", 'children')]
              
)

def stock_results(ticker1,ticker2,days,c1,c2,c3):

    stock1 = stock_comp(ticker1,days)
    stock2 = stock_comp(ticker2,days)

    dataframe = pd.merge(stock1.df_company, stock2.df_company)

    

    # dataframe.set_index('Date',inplace = True)

    correlation = dataframe.corr()

    
    
    graph = px.line(dataframe, x = 'Date' , y = [ticker1,ticker2], title='Value of stocks over time').update_layout(
        template='plotly_dark',
        plot_bgcolor= 'rgba(0, 0, 0, 0)',
        paper_bgcolor= 'rgba(0, 0, 0, 0)',)
    
    return [dcc.Graph(figure = graph), correlation.to_dict(orient='records'), dataframe.to_dict(orient='records')]



if __name__ == '__main__':
    app.run_server( host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False) 

