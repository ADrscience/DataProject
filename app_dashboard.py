
# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

data="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(data)
spacex_df.head()




#Task 1,2,3,4
#===============================================================================================================================================
# List of options for the Dropdown component.
# Each option is a dictionary with two keys:
# 'label': The text the user will see in the dropdown list.
# 'value': The internal value used in the code (e.g., for filtering data) when the user selects that option.
options = [
	{'label': 'All Sites', 'value': 'ALL'},           # Option to represent all launch sites.
	{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, # Option for the specific site CCAFS LC-40.
	{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, # Option for the specific site VAFB SLC-4E.
	{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},   # Option for the specific site KSC LC-39A.
	{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}# Option for the specific site CCAFS SLC-40.
]

# Define a default color sequence from Plotly Express.
# This can be used by px charts to assign colors to different categories.
color_sequence = px.colors.qualitative.Plotly

# Determine the maximum value of the 'Payload Mass (kg)' column in the spacex_df DataFrame.
# This will be used to set the upper limit of the RangeSlider.
max_payload = spacex_df['Payload Mass (kg)'].max()

# Determine the minimum value of the 'Payload Mass (kg)' column in the spacex_df DataFrame.
# This will be used to set the lower limit of the RangeSlider.
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create an instance of the Dash app.
# `__name__` is a special Python variable that Dash uses for proper app configuration.
app = dash.Dash(__name__)

# Define the layout of the Dash app UI.
# The layout is defined as a tree of Dash components (HTML and Core Components).
# The main component is an html.Div containing all other elements.
app.layout = html.Div(children=[

	# HTML H1 component to display the main dashboard title.
	html.H1('SpaceX Launch Records Dashboard',
			style={'textAlign': 'center',
				   'color': '#503D36',
				   'font-size': 40}),

	# A Div containing the Label and Dropdown for launch site selection.
	html.Div([
		html.Label("Select a Launch Site", style={'color': 'Blue', 'font-size': 20}),
		dcc.Dropdown(
			id='site-dropdown',
			options=options,
			value='ALL',
			placeholder='Select a Launch Site here',
			searchable=True
		)
	],
	style={
		'width': '50%',
		'display': 'inline-block'
	}),

	# HTML Br component for vertical spacing.
	html.Br(),

	# A Div containing the pie chart (Pie Chart).
	html.Div(dcc.Graph(
		id='success-pie-chart',
		style={
			'display': 'flex',
			'flex-wrap': 'wrap',
			'justify-content': 'center',
			'gap': '20px'
		}
	)),
 #================================================================================================================================
	# HTML Br component for more vertical spacing.
	html.Br(),
 #==================================================================================================================================

	# TASK 3: Add a slider to select payload range
	# Original comment indicating the task related to the RangeSlider.
	#dcc.RangeSlider(id='payload-slider',...) # Original comment showing part of the code to be added.

	# A main Div containing the RangeSlider section.
	html.Div([
		html.Div([
			html.Label(
				"Select Payload Mass Range (kg)",
				style={'color': 'Blue', 'font-size': 15}
			),
			html.Br(),
			html.Br(),
			dcc.RangeSlider(
				id='payload-slider',
				min=0,
				max=10000,
				step=1000,
				marks={i: f'{i}kg' for i in range(0, 10001, 2500)},
				value=[min_payload, max_payload]
			)
		])
	]),

	# TASK 4: Add a scatter chart to show the correlation between payload and launch success
	# Original comment indicating the task related to the scatter plot.
	# html.Div(dcc.Graph(id='success-payload-scatter-chart')), # Original comment showing the component to be added.

	# A Div containing the scatter plot.
	html.Div(dcc.Graph(
		id='success-payload-scatter-chart',
		style={
			'display': 'flex',
			'flex-wrap': 'wrap',
			'justify-content': 'center',
			'gap': '20px'
		}))
]) # End of app layout definition.

#=============================================================================================================================================
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Original comment indicating the task and a note about multiple callbacks.
# For dashboards with more than one chart, it is recommended to use a callback with multiple outputs.

# Callback definition: Connects Inputs with Outputs.
# The @app.callback decorator registers the uptade_graph function to be executed
# automatically when the value of any of the specified Inputs changes.
@app.callback(
	# List of Outputs: Defines which components and which properties will be updated.
	[Output(component_id='success-pie-chart', component_property='figure'),
	 Output(component_id='success-payload-scatter-chart', component_property='figure')],

	# List of Inputs: Defines which components and properties will trigger the callback.
	[Input(component_id='site-dropdown', component_property='value'),
	 Input(component_id='payload-slider', component_property='value')]
)
# The function that runs when the callback is triggered.
# The function arguments receive the current values of the specified Input properties, in the same order.
def uptade_graph(entered_site, payload_range):
	# 1) Create a copy of the original DataFrame (`spacex_df`).
	# It's good practice to work with a copy to avoid modifying the global DataFrame inside the callback.
	filtered_df = spacex_df.copy()

	# 2) Filter the DataFrame by launch site if a specific one is selected.
	# If the dropdown value (`entered_site`) is not 'ALL', filter the DataFrame
	# to only include rows where 'Launch Site' matches the selected site.
	if entered_site != 'ALL':
		filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
  

	# 3) Filter the DataFrame by payload mass range.
	# If `payload_range` (a list with [min, max] from the slider) is not None,
	# filter the DataFrame to only include rows where 'Payload Mass (kg)' is between
	# the selected min (`payload_range[0]`) and max (`payload_range[1]`) values.
	if payload_range is not None:
		filtered_df = filtered_df[
			(filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
			(filtered_df['Payload Mass (kg)'] <= payload_range[1])
		]

	# 4) Generate the pie chart with Plotly Express.
	# Use the filtered DataFrame (`filtered_df`).
	pie_fig = px.pie(
		filtered_df,
		names='class',
		title=(
			'Success vs Failure for All Sites'
			if entered_site == 'ALL'
			else f'Success vs Failure for site {entered_site}'
		)
	)

	# 5) Update pie chart labels for clarity.
	# By default, Plotly uses the unique values of the 'names' column (0 and 1) as labels.
	# `update_traces` allows modifying chart properties.
	# Here, labels '0' are replaced with 'Not Success' and '1' with 'Success'.
	pie_fig.update_traces(
		labels=[
			'Not Success' if val == 0
			else 'Success'
			for val in pie_fig.data[0].labels
		]
	)

	# 6) Generate the scatter plot with Plotly Express.
	# Use the same filtered DataFrame (`filtered_df`).
	scatter_fig = px.scatter(
		filtered_df,
		x="Payload Mass (kg)",
		y="class",
		color="Booster Version Category",
		hover_name="Booster Version Category",
		title='Relationship between Payload Mass and Launch Success',
		size_max=60
	)

	# 7) Return the generated figures.
	# The values returned by the callback function are assigned to the properties
	# of the components specified in the Outputs list, in the same order.
	return pie_fig, scatter_fig

# Standard Python entry point.
# The code inside this block only runs if the script is executed directly
# (and not if it is imported as a module in another script).
if __name__ == '__main__':
	# Start the Dash development server.
	# This makes the app accessible via a web browser (usually at http://127.0.0.1:8050/).
    app.run_server(debug=True)