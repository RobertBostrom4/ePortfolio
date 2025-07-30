from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Setup the Jupyter version of Dash
from dash import Dash
app = Dash(__name__)


# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from crud_module import AnimalDatabaseManager

###########################
# Data Manipulation / Model
###########################

# MongoDB credentials and connection setup

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")
port = int(os.getenv("MONGO_PORT"))
db_name = os.getenv("MONGO_DB")

# Connect to database via CRUD Module
db = AnimalDatabaseManager()

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)


## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)

# Below are all of the filtering queries for the interactive options

# Query for Water Rescue filter
def water_rescue_query():
    return {
        "animal_type": "Dog",
        "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
        "sex_upon_outcome": "Intact Female",
        "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
    }


# Query for Mountain or Wilderness Rescue filter
def mountain_rescue_query():
    return {
        "animal_type": "Dog",
        "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
    }
# Query for Disaster or Tracking filter
def disaster_tracking_query():
    return {
        "animal_type": "Dog",
        "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
        "sex_upon_outcome": "Intact Male",
        "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
    }



#########################
# Dashboard Layout / View
#########################
app = Dash(__name__)


#Grazioso Salvare’s logo
image_filename = 'Grazioso Salvare Logo.png'

app.layout = html.Div([
    # Company Logo and my name as header
    html.Div([
        html.Img(src='/assets/Grazioso Salvare Logo.png', height='100px'),
        html.H3("CS-340 Dashboard - Robert Bostrom")
    ], style={'textAlign': 'center'}),

    html.Hr(),
        
#Interactive filtering options. I've chosen radio buttons.

    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Water Rescue', 'value': 'WATER'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'MOUNTAIN'},
            {'label': 'Disaster or Individual Tracking', 'value': 'DISASTER'},
            {'label': 'Reset', 'value': 'RESET'}
        ],
        value='RESET', # Default selected
        labelStyle={'display': 'block'} # Vertical list layout
    ),

    html.Hr(),
# Data table
    dash_table.DataTable(
            id='datatable-id',
            columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            row_selectable="single", # Only one row can be selected at a time
            selected_rows=[0], # Default selected row
            sort_action="native", # Enable sorting
            filter_action="native" # Enable filtering
        ),

        html.Br(), html.Hr(),
# Dashboard so that the chart and the geolocation chart are side-by-side
    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(id='graph-id', className='col s12 m6'), # Pie chart output
        html.Div(id='map-id', className='col s12 m6') # Map output
    ])
])

#############################################
# Interaction Between Components / Controller
#############################################
    
@app.callback(
    Output('datatable-id', 'data'),
    [Input('filter-type', 'value')]
)

def update_dashboard(filter_type):
    # Determine which query to use
    if filter_type == 'WATER':
        results = db.read(water_rescue_query())
    elif filter_type == 'MOUNTAIN':
        results = db.read(mountain_rescue_query())
    elif filter_type == 'DISASTER':
        results = db.read(disaster_tracking_query())
    else:  # RESET or unrecognized input
        results = db.read({}) # No filter, return all

    # Clean and return results as dictionary records for DataTable
    df_local = pd.DataFrame.from_records(results)
    if '_id' in df_local.columns:
        df_local['_id'] = df_local['_id'].astype(str)

    return df_local.to_dict('records')

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):
    
    if viewData is None:
        return []
    
     # Convert the filtered data to DataFrame
    dff = pd.DataFrame(viewData)
    if dff.empty or 'breed' not in dff.columns:
        return []

    # Display pie chart of breeds from filtered results
    return [
        dcc.Graph(
            figure=px.pie(dff, names='breed', title='Breed Distribution of Filtered Results')
        )
    ]

    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    if selected_columns is None:
        return []

    # Highlight selected column(s) with light blue background
    return [{
        'if': {'column_id': col},
        'background_color': '#D2F3FF'
    } for col in selected_columns]



# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")]
)
def update_map(viewData, index):
    if viewData is None or not index:
        return []

    # Convert table data to DataFrame
    dff = pd.DataFrame.from_dict(viewData)
    row = index[0] if index else 0

    try:
        # Extract geolocation and display info
        lat = float(dff.iloc[row]['location_lat'])
        lon = float(dff.iloc[row]['location_long'])
        breed = dff.iloc[row]['breed']
        name = dff.iloc[row]['name']
    except:
        # Fallback location if data is missing
        lat, lon, breed, name = 30.75, -97.48, "Unknown", "Unknown"

        # Return leaflet map with a single marker and popup
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[lat, lon], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(position=[lat, lon], children=[
                dl.Tooltip(breed),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(name)
                ])
            ])
        ])
    ]




app.run(debug=True)
