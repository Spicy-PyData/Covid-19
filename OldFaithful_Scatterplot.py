import numpy as np
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State


df = pd.read_csv('OldFaithful.csv')


# Css Styles
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}








app = dash.Dash()


app.layout = html.Div([
                        dcc.Tabs(id="tabs", value='tab-1',
                        children=[dcc.Tab(label='Tab one', value='tab-1', style=tab_style,selected_style=tab_selected_style),
                                    dcc.Tab(label='Tab two', value='tab-2', style=tab_style,selected_style=tab_selected_style)],
                        style=tabs_styles),

                        html.Div(id='show-tabs-content'),


                                            ])




@app.callback(Output('show-tabs-content', 'children'),
              [Input('tabs', 'value')])

def render_content(tab):
    value = 'OldFaithful'
    if tab == 'tab-1':
        return html.Div([dcc.Graph(id='OldFaithful',
                                figure = {'data':[go.Scatter(x=df['X'],y=df['Y'],mode='markers',
                                marker=dict(symbol='pentagon',size=12,color='rgb(50,200,50')
                                )],
                                'layout':go.Layout(title='Old Faithful',
                                                    xaxis=dict(title='Duration'),yaxis=dict(title='Time until Next')),
                                                    })])

    elif tab == 'tab-2':
        return html.Div(html.H3('Tab content 2'))



if __name__ == '__main__':
    app.run_server()
