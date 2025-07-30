from __future__ import annotations

# --- Load env vars early so that DB credentials are available before imports that need them.
from dotenv import load_dotenv
import os
load_dotenv()

# Dash framework imports
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State

# Dashboard components
import dash_leaflet as dl
import plotly.express as px

# Data / numeric stack
import pandas as pd
import numpy as np

# Local DB manager
from crud_module import AnimalDatabaseManager


# ---------------------------------------------------------
# Global configuration
# ---------------------------------------------------------
# Toggling this means we want *all* filtering to come from MongoDB queries instead of in-memory.
USE_DB_FILTERS = False

# Fields we actually need in the dashboard. Projecting only these reduces network cost and RAM.
REQUIRED_FIELDS = [
    "name",
    "breed",
    "animal_type",
    "sex_upon_outcome",
    "age_upon_outcome_in_weeks",
    "location_lat",
    "location_long",
]

# Default sort: youngest first (ascending age). Change to descending if desired.
DEFAULT_SORT_FIELD = "age_upon_outcome_in_weeks"
DEFAULT_SORT_ASC = True


# ---------------------------------------------------------
# Database Connection + Initial Load
# ---------------------------------------------------------
# NOTE: Credentials are pulled from environment variables via .env.
# We construct the db object with no args because the class itself reads env vars internally.
db = AnimalDatabaseManager()


def load_base_df(force_refresh: bool = False) -> pd.DataFrame:
    """Load the base dataset (all animals) with projection + cleanup.

    We centralize this so that:
      * We only hit the DB once at startup (or when explicitly refreshed).
      * We apply consistent cleanup (drop _id, cast numbers, strip strings).
      * We sort the data for a stable user experience.

    Parameters
    ----------
    force_refresh : bool
        If True, bypasses cache and re-reads from MongoDB.

    Returns
    -------
    pd.DataFrame
    """
    # The DB helper exposes a cached read_df() that already projects + cleans.
    df_all = db.read_df({}, fields=REQUIRED_FIELDS, force_refresh=force_refresh)

    # Sort (vectorized, O(n log n), negligible at our scale).
    if DEFAULT_SORT_FIELD in df_all.columns:
        df_all = df_all.sort_values(by=DEFAULT_SORT_FIELD, ascending=DEFAULT_SORT_ASC, ignore_index=True)

    return df_all


# Load once at import time. For big datasets you might lazy-load in a callback.
BASE_DF = load_base_df(force_refresh=False)


# ---------------------------------------------------------
# Filter Query Specs – algorithms expressed as data
# ---------------------------------------------------------
# Instead of scattering Mongo-style dicts everywhere, define filter specs in one place.
# Each entry defines allowed breeds, required sex, and age window. We can apply these either by
# pushing the filter down to MongoDB OR performing a vectorized mask over the local DataFrame.

FILTER_SPECS = {
    "WATER": {
        "breeds": {"Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"},
        "sex": "Intact Female",
        "age_min": 26,
        "age_max": 156,
    },
    "MOUNTAIN": {
        "breeds": {"German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"},
        "sex": "Intact Male",
        "age_min": 26,
        "age_max": 156,
    },
    "DISASTER": {
        "breeds": {"Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"},
        "sex": "Intact Male",
        "age_min": 20,
        "age_max": 300,
    },
}


def spec_to_mongo_query(spec_key: str) -> dict:
    """Translate a FILTER_SPECS entry into a MongoDB query dict.

    Used when USE_DB_FILTERS=True.
    """
    spec = FILTER_SPECS[spec_key]
    return {
        "animal_type": "Dog",  # All three searches are for dogs in original requirements.
        "breed": {"$in": sorted(list(spec["breeds"]))},
        "sex_upon_outcome": spec["sex"],
        "age_upon_outcome_in_weeks": {"$gte": spec["age_min"], "$lte": spec["age_max"]},
    }


def apply_spec_filter(df: pd.DataFrame, spec_key: str) -> pd.DataFrame:
    """Vectorized in-memory filter that applies a FILTER_SPECS rule to a DataFrame.

    This is O(n) over the DataFrame instead of a network round-trip to MongoDB.
    Efficient set membership (`.isin()`) + boolean masking.
    """
    spec = FILTER_SPECS[spec_key]

    # Guard against missing columns.
    cols = df.columns
    if not {"breed", "sex_upon_outcome", "age_upon_outcome_in_weeks"}.issubset(cols):
        return df.iloc[0:0]  # empty

    mask = (
        df["breed"].isin(spec["breeds"]) &
        (df["sex_upon_outcome"] == spec["sex"]) &
        (df["age_upon_outcome_in_weeks"] >= spec["age_min"]) &
        (df["age_upon_outcome_in_weeks"] <= spec["age_max"])
    )
    return df.loc[mask].copy()


# Simple memo cache for filtered results so repeat clicks are instant.
_filter_cache: dict[str, pd.DataFrame] = {}


def get_filtered_df(filter_type: str) -> pd.DataFrame:
    """Return filtered DataFrame for the given filter type.

    * If RESET → return the base dataset.
    * If cached → return cached copy.
    * Else compute (either DB query or in-memory mask depending on USE_DB_FILTERS flag).
    * Cache the result.
    """
    filter_type = (filter_type or "RESET").upper()

    if filter_type == "RESET":
        return BASE_DF

    if filter_type in _filter_cache:
        return _filter_cache[filter_type]

    if USE_DB_FILTERS:
        # Query MongoDB directly (projection + cleanup happens in read_df).
        df_f = db.read_df(spec_to_mongo_query(filter_type), fields=REQUIRED_FIELDS)
    else:
        # In-memory vectorized filtering.
        df_f = apply_spec_filter(BASE_DF, filter_type)

    _filter_cache[filter_type] = df_f
    return df_f


# ---------------------------------------------------------
# Dash Layout
# ---------------------------------------------------------

app = Dash(__name__)
server = app.server 

app.layout = html.Div([
    # Header / branding
    html.Div([
        html.Img(src='/assets/Grazioso Salvare Logo.png', height='100px'),
        html.H3("CS-340 Dashboard - Robert Bostrom")
    ], style={'textAlign': 'center'}),

    html.Hr(),

    # Filter radio buttons
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'Water Rescue', 'value': 'WATER'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'MOUNTAIN'},
            {'label': 'Disaster or Individual Tracking', 'value': 'DISASTER'},
            {'label': 'Reset', 'value': 'RESET'}
        ],
        value='RESET',  # Default selected
        labelStyle={'display': 'block'}  # Vertical list layout
    ),

    html.Hr(),

    # Hidden store: keep the *current* filtered table rows in browser memory.
    # This allows downstream callbacks (chart + map) to avoid requesting DB/data again.
    dcc.Store(id='store-table-data', data=BASE_DF.to_dict('records')),

    # Data table
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": c, "id": c, "deletable": False, "selectable": True} for c in BASE_DF.columns],
        data=BASE_DF.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        row_selectable="single",  # Only one row can be selected at a time
        selected_rows=[0],  # Default selected row
        sort_action="native",  # Enable client-side sorting
        filter_action="native"  # Enable client-side filtering
    ),

    html.Br(), html.Hr(),

    # Dashboard row: chart + map side-by-side
    html.Div(className='row', style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
        html.Div(id='graph-id', className='col s12 m6', style={'flex': '1 1 50%'}),  # Pie chart output
        html.Div(id='map-id', className='col s12 m6', style={'flex': '1 1 50%'})    # Map output
    ])
])


# ---------------------------------------------------------
# Callbacks
# ---------------------------------------------------------

@app.callback(
    Output('datatable-id', 'data'),
    Output('store-table-data', 'data'),  # keep store in sync
    Input('filter-type', 'value')
)
def update_dashboard(filter_type):
    """Update the DataTable based on selected filter.

    * Uses cached / in-memory filtering for responsiveness (Category 2 enhancement).
    * Also updates a hidden dcc.Store so downstream callbacks don't recompute.
    """
    df_local = get_filtered_df(filter_type)
    # Dash DataTable requires JSON-serializable types; convert here.
    records = df_local.to_dict('records')
    return records, records


@app.callback(
    Output('graph-id', 'children'),
    Input('store-table-data', 'data')
)
def update_graphs(viewData):
    """Update pie chart showing breed distribution of current table rows.

    Because the table data is already filtered and stored in-browser, this callback does
    *no* additional DB work. We simply re-aggregate using vectorized pandas `value_counts`.
    """
    if not viewData:
        return []

    dff = pd.DataFrame(viewData)
    if dff.empty or 'breed' not in dff.columns:
        return []

    # Group & count – O(n). Equivalent to `dff.groupby('breed').size()` but value_counts is concise.
    breed_counts = dff['breed'].value_counts().reset_index(name='count').rename(columns={'index': 'breed'})

    fig = px.pie(breed_counts, names='breed', values='count', title='Breed Distribution of Filtered Results')

    return [dcc.Graph(figure=fig)]


@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    Input('datatable-id', 'selected_columns')
)
def update_styles(selected_columns):
    """Highlight selected column(s) in light blue."""
    if not selected_columns:
        return []
    return [{
        'if': {'column_id': col},
        'background_color': '#D2F3FF'
    } for col in selected_columns]


@app.callback(
    Output('map-id', 'children'),
    Input('store-table-data', 'data'),
    Input('datatable-id', 'derived_virtual_selected_rows'),
)
def update_map(viewData, selected_rows):
    """Update map to show the currently selected animal's location.

    We pull from the *stored* table data rather than re-reading DB. This is a key
    data-structure win: the browser already has the dataset; re-using it avoids network I/O.
    """
    if not viewData:
        return []

    dff = pd.DataFrame(viewData)

    # Selected_rows is a list (DataTable always passes a list). Default = first row.
    row_index = selected_rows[0] if selected_rows else 0
    if row_index >= len(dff):
        row_index = 0

    # Defensive extraction with fallbacks.
    try:
        lat = float(dff.iloc[row_index].get('location_lat', 30.75))
        lon = float(dff.iloc[row_index].get('location_long', -97.48))
        breed = dff.iloc[row_index].get('breed', 'Unknown')
        name = dff.iloc[row_index].get('name', 'Unknown')
    except Exception:
        lat, lon, breed, name = 30.75, -97.48, 'Unknown', 'Unknown'

    return [
        dl.Map(style={'width': '100%', 'height': '500px'}, center=[lat, lon], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            dl.Marker(position=[lat, lon], children=[
                dl.Tooltip(breed),
                dl.Popup([html.H1("Animal Name"), html.P(name)])
            ])
        ])
    ]


# ---------------------------------------------------------
# Main Entrypoint
# ---------------------------------------------------------
if __name__ == '__main__':
    # debug=True gives live reload; change to False in production.
    app.run(debug=True)