'''
 # @ Create Time: 2024-05-07 18:58:23.931626
'''
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import matplotlib as mpl
import plotly.express as px
import plotly.graph_objects as go

#import seaborn as sns

from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# import the dataset

import pandas as pd

# Define a list of URLs
urls = [
    'https://drive.google.com/file/d/19-k-w_16gRIvjVCwo6T9aHEN8oEBOd85/view?usp=share_link',
    'https://drive.google.com/file/d/1nuFo9cavPYC0_bzCrQ2P0xVFw_KvtGVs/view?usp=share_link',
    'https://drive.google.com/file/d/1iWT7rLqu_V9-IHn3J9F6iIYTHD1G_ILo/view?usp=share_link',
    'https://drive.google.com/file/d/1vXgudhkOpKp09X2PyOcKFWmmV6c5AGOm/view?usp=share_link',
    'https://drive.google.com/file/d/1W9u4Ho8orcMaNI9V0qK49tlxjAwcCtEr/view?usp=share_link',
    'https://drive.google.com/file/d/1cP-B8HTRjiWXi7J-aKLI_n1vZFU_koLl/view?usp=share_link'
    #'https://drive.google.com/file/d/1f0NjWwQAzrXHl8mA_d5IniUfxaPR5BF1/view?usp=share_link',
    #'https://drive.google.com/file/d/1xgluvB1ZlhvvVQoO_XZZWXqGEH3IK3Pj/view?usp=share_link',
    #'https://drive.google.com/file/d/1_8ySbnwcK9XYaIKMcNVq4H4hnbAtE7yz/view?usp=share_link',
    #'https://drive.google.com/file/d/1_8ySbnwcK9XYaIKMcNVq4H4hnbAtE7yz/view?usp=share_link', #10
    # Add more URLs as needed
]

# Initialize an empty list to store DataFrames
dfs = []

# Loop through each URL
for url in urls:
    # Modify the URL to use the direct download link
    url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
    
    # Read the CSV file directly from the URL into a DataFrame
    df1 = pd.read_csv(url)
    
    # Append the DataFrame to the list
    dfs.append(df1)

# Concatenate all DataFrames into a single DataFrame
df = pd.concat(dfs, ignore_index=True)

# Now you can work with the combined DataFrame
#print(combined_df.head())

#df1 = pd.read_csv("https://raw.githubusercontent.com/turingzhi/dash1/main/taxi1.csv")

#df2 = pd.read_csv("https://raw.githubusercontent.com/turingzhi/dash1/main/taxi2.csv")

#df = pd.read_csv('taxi3.csv')
#df= pd.read_csv("https://raw.githubusercontent.com/turingzhi/dash1/main/taxi3.csv")

#url='https://drive.google.com/file/d/19-k-w_16gRIvjVCwo6T9aHEN8oEBOd85/view?usp=share_link'
#url='https://drive.google.com/uc?id=' + url.split('/')[-2]
#df = pd.read_csv(url)

# Merge the DataFrames based on a common column (e.g., 'key_column')
# Replace 'key_column' with the actual column(s) you want to use for merging
#df = pd.concat([df1, df2], ignore_index=True)
#df = df.drop(df.columns[:2], axis=1)
df = df.drop(['Trip ID', 'Taxi ID', 'Trip End Timestamp','Payment Type','Company','Pickup Centroid Location','Dropoff Centroid  Location','Pickup Census Tract','Dropoff Census Tract'], axis=1)
# delete rows containing the Nan
df = df.dropna(subset=['Pickup Community Area','Dropoff Community Area'])
# transform the type into 'int'
df['Pickup Community Area'] = df['Pickup Community Area'].astype(int)
df['Dropoff Community Area'] = df['Dropoff Community Area'].astype(int)
df['Trip Start Timestamp'] = pd.to_datetime(df['Trip Start Timestamp'])



# Create Dash app
app1 = Dash(__name__)


server = app1.server
# App layout
app1.layout = html.Div([
    html.Div([
        dcc.Slider(
            id='hour-slider',
            min=0,
            max=23,
            value=0,  # Default value is 0
            marks={i: f'{i}h' for i in range(24)},  # Marks from 0h to 23h, every hour
            step=1,  # Slider step is 1 hour
        ),
    ], style={'margin': '9px'}),
    html.Link(
        rel='stylesheet',
        href='../assets/style.css'
    ),
    dcc.Graph(id='map-graph')  # Graph
], style={'width': '600px', 'height': '400px'})  #   Adjust width and height here

# Callback function, update graph
@app1.callback(
    Output('map-graph', 'figure'),
    [Input('hour-slider', 'value')]
)
def update_map(selected_hour):
    df['Trip Start Timestamp'] = pd.to_datetime(df['Trip Start Timestamp'], errors='coerce')
    filtered_df = df[df['Trip Start Timestamp'].dt.hour == selected_hour]

    # Create map scatter plot
    fig = px.scatter_mapbox(filtered_df,
                           lat='Pickup Centroid Latitude',
                           lon='Pickup Centroid Longitude',
                           color_continuous_scale='Viridis',
                           mapbox_style='carto-positron',
                           zoom=9,
                           center={"lat": 41.8781, "lon": -87.6298},
                           opacity=0.5,
                           labels={'Population': 'Population Count'})
    fig.update_layout(height=600, width=600)
    return fig

# Run app
if __name__ == '__main__':
    app1.run_server(debug=True, port=8050)  # Run on local server, enable debug mode
