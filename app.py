import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import random

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP,],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

data = pd.read_csv('data.csv')
df = pd.DataFrame(data)

# Chart 1: Weather Conditions vs. Accident Counts
weather_accident_counts = df.groupby("Weather_Condition").size().reset_index(name="Accident_Count")
fig1 = px.bar(
    weather_accident_counts,
    x="Weather_Condition",
    y="Accident_Count",
    labels={"Accident_Count": "Number of Accidents", "Weather_Condition": "Weather Condition"},
    color="Weather_Condition",
    text="Accident_Count",
    color_discrete_sequence=["#115f9a", "#1984c5", "#22a7f0", "#48b5c4", "#FF7F3E"]
)


# Chart 2: Regional Accident Distribution Map
regional_accidents = df.groupby("state_code").size().reset_index(name="Accident_Count")

fig2 = px.choropleth(
    regional_accidents,
    locations="state_code",  
    locationmode="USA-states",
    color="Accident_Count",
    scope="usa",
    labels={"Accident_Count": "Number of Accidents", "state_code": "State"},
    color_continuous_scale="blues",  
    hover_data=["state_code", "Accident_Count"] 
)

# Chart 3: Time-of-Day Trends in Different Weather
time_weather_accidents = df.groupby(["Year", "Weather_Condition"]).size().reset_index(name="Accident_Count")
fig3 = px.line(
    time_weather_accidents,
    x="Year",
    y="Accident_Count",
    color="Weather_Condition",
    labels={"Accident_Count": "Number of Accidents", "Year": "Year"},
    markers=True,
    color_discrete_sequence=["#115f9a", "#1984c5", "#22a7f0", "#48b5c4", "#76c68f"]
)


app.layout = html.Div([
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1([
                            "Making Roads Safer",
                            html.Br(),
                            "Through Weather ",
                            html.Span("Intelligence", style={
                                "color": "#115f9a",
                                "background": "linear-gradient(120deg, #D4EBF8 0%, #D4EBF8 100%)",
                                "background-repeat": "no-repeat",
                                "background-size": "100% 0.2em",
                                "background-position": "0 88%"
                            }),
                        ], className="display-4 fw-bold lh-1 mb-3"),
                        html.P(
                            "Explore analytics on how weather patterns impact road safety across the United States. "
                            "Make informed decisions with data-driven insights.",
                            className="lead fw-normal text-muted mb-4"
                        ),
                        dbc.Button([
                            "View Methodology ",
                            html.I(className="fas fa-arrow-right ms-2")
                        ], color="primary", size="lg", className="rounded-pill px-4"),
                    ], className="py-5"),
                ], md=7),
                
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-cloud-sun-rain", 
                                  style={"font-size": "4rem", "color": "#115f9a"}),
                            html.I(className="fas fa-car-side mx-3", 
                                  style={"font-size": "3rem", "color": "#98DED9"}),
                            html.I(className="fas fa-chart-line", 
                                  style={"font-size": "4rem", "color": "#161D6F"}),
                        ], className="d-flex align-items-center justify-content-center")
                    ], className="hero-illustration p-4 text-center")
                ], md=5, className="d-flex align-items-center"),
            ], className="align-items-center")
        ], fluid="lg", className="px-4")
    ], className="hero-section py-5 mb-4", style={
        "background": "linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%)",
        "backdrop-filter": "blur(10px)",
        "-webkit-backdrop-filter": "blur(10px)",
        "border-bottom": "1px solid rgba(0,0,0,0.1)",
        "box-shadow": "0 4px 20px rgba(0,0,0,0.05)"
    }),
    
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Filter Data", className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select Region", className="mb-2"),
                                dcc.Dropdown(
                                    id='region-filter',
                                    options=[{'label': region, 'value': region} for region in sorted(df['Region'].unique())],
                                    value='All',
                                    multi=True,
                                    placeholder="Select regions...",
                                    className="mb-3"
                                ),
                            ], md=6),
                            dbc.Col([
                                html.Label("Select Year", className="mb-2"),
                                dcc.Dropdown(
                                    id='year-filter',
                                    options=[{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                                    value='All',
                                    multi=True,
                                    placeholder="Select years...",
                                    className="mb-3"
                                ),
                            ], md=6),
                        ]),
                    ])
                ], className="mb-4 filter-card")
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Current Weather Impact Summary"),
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-cloud-sun fa-3x mb-3"),
                            html.H4(id="total-accidents"),
                            html.P(id="common-weather")
                        ], className="text-center")
                    ])
                ])
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Accident Severity Overview"),
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-exclamation-triangle fa-3x mb-3"),
                            html.H4(id="fatal-accidents"),
                            html.P(id="common-time")
                        ], className="text-center")
                    ])
                ])
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Temperature Analysis"),
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-temperature-high fa-3x mb-3"),
                            html.H4(id="avg-temperature"),
                            html.P(id="temp-range")
                        ], className="text-center")
                    ])
                ])
            ], md=4),
        ], className="mb-4"),
        
        # Main content
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Accidents by Weather Condition"),
                        dbc.CardBody([
                            dcc.Graph(id='weather-chart', figure=fig1, config={'displayModeBar': False})
                        ])
                    ])
                ], md=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Regional Accident Distribution"),
                        dbc.CardBody([
                            dcc.Graph(id='map-chart', figure=fig2, config={'displayModeBar': False})
                        ])
                    ])
                ], md=6),
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Time-of-Day Trends by Weather Condition"),
                        dbc.CardBody([
                            dcc.Graph(id='trend-chart', figure=fig3, config={'displayModeBar': False})
                        ])
                    ])
                ], md=12),
            ]),
        ], fluid=True)
    ]),
])

@app.callback(
    [Output('weather-chart', 'figure'),
     Output('map-chart', 'figure'),
     Output('trend-chart', 'figure'),
     Output('total-accidents', 'children'),
     Output('common-weather', 'children'),
     Output('fatal-accidents', 'children'),
     Output('common-time', 'children'),
     Output('avg-temperature', 'children'),
     Output('temp-range', 'children')],
    [Input('region-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_charts(selected_regions, selected_years):
    # Filter the dataframe based on selections
    dff = df.copy()
    
    if selected_regions != 'All' and selected_regions:
        if isinstance(selected_regions, str):
            dff = dff[dff['Region'] == selected_regions]
        else:
            dff = dff[dff['Region'].isin(selected_regions)]
            
    if selected_years != 'All' and selected_years:
        if isinstance(selected_years, (int, float)):
            dff = dff[dff['Year'] == selected_years]
        else:
            dff = dff[dff['Year'].isin(selected_years)]

    # Update Chart 1: Weather Conditions
    weather_accident_counts = dff.groupby("Weather_Condition").size().reset_index(name="Accident_Count")
    fig1 = px.bar(
        weather_accident_counts,
        x="Weather_Condition",
        y="Accident_Count",
        labels={"Accident_Count": "Number of Accidents", "Weather_Condition": "Weather Condition"},
        color="Weather_Condition",
        text="Accident_Count",
        color_discrete_sequence=['#80C4E9']
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#161D6F',
        showlegend=False,
    )
    fig1.update_xaxes(showgrid=False)
    fig1.update_yaxes(gridcolor='rgba(152, 222, 217, 0.2)')

    # Update Chart 2: Map
    regional_accidents = dff.groupby("state_code").size().reset_index(name="Accident_Count")
    fig2 = px.choropleth(
        regional_accidents,
        locations="state_code",
        locationmode="USA-states",
        color="Accident_Count",
        scope="usa",
        labels={"Accident_Count": "Number of Accidents", "state_code": "State"},
        color_continuous_scale=[[0, '#C7FFD8'], [0.5, '#98DED9'], [1, '#161D6F']],
        hover_data=["state_code", "Accident_Count"]
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#161D6F',
        margin=dict(l=0, r=0, t=30, b=0)
    )

    # Update Chart 3: Time Trends
    time_weather_accidents = dff.groupby(["Year", "Weather_Condition"]).size().reset_index(name="Accident_Count")
    fig3 = px.line(
        time_weather_accidents,
        x="Year",
        y="Accident_Count",
        color="Weather_Condition",
        labels={"Accident_Count": "Number of Accidents", "Year": "Year"},
        markers=True,
        color_discrete_sequence=['#161D6F', '#0B2F9F', '#98DED9', '#229799', '#EC8305']
    )
    fig3.update_xaxes(
        dtick=1,
        tick0=df['Year'].min(),
        tickmode='linear',
        type='category'
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#161D6F',
    )
    fig3.update_xaxes(showgrid=False)
    fig3.update_yaxes(gridcolor='rgba(152, 222, 217, 0.2)')

    fig3.update_traces(line=dict(width=3)) 

    # Calculate summary card values
    total_accidents = f"Total Accidents: {len(dff):,}"
    common_weather = f"Most Common Weather: {dff['Weather_Condition'].mode()[0]}"
    fatal_accidents = f"Fatal Accidents: {len(dff[dff['Severity'] == 'Fatal']):,}"
    common_time = f"Most Common Time: {dff['Time_of_Day'].mode()[0]}"
    avg_temp = f"Avg. Temperature: {dff['Region_Temperature'].mean():.1f}°C"
    temp_range = f"Temperature Range: {dff['Region_Temperature'].min():.1f}°C to {dff['Region_Temperature'].max():.1f}°C"

    return fig1, fig2, fig3, total_accidents, common_weather, fatal_accidents, common_time, avg_temp, temp_range

if __name__ == '__main__':
    app.run(debug=True)

