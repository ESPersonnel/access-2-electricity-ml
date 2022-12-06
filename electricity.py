# Import the necessary libraries

import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

# Create a Flask app

app = Flask(__name__)

# Define a function to get the data from the API

def get_data():
    # Make an API call and store the response
    url = 'http://api.worldbank.org/v2/countries/all/indicators/EG.ELC.ACCS.ZS?date=2000:2021&format=json'
    r = requests.get(url)
    # Process the response
    response_dict = r.json()
    # Extract the data from the response
    data = response_dict[1]
    # Return the data
    return data

# Define a function to format the data

def format_data(data):
    # Create a new dataset
    df = pd.DataFrame(columns=['Country', 'Year', 'Access to electricity'])
    # Loop through the data and extract the data for each country and year
    for country in data:
        for year in country['date']:
            # Extract the country name
            country_name = country['country']['value']
            # Extract the year
            year = year
            # Extract the access to electricity data
            access_to_electricity = country['value']
            # Append the data to the new dataset
            df = df.append({'Country': country_name, 'Year': year, 'Access to electricity': access_to_electricity}, ignore_index=True)
    # Return the new dataset
    return df

# Define a function to create the scatterplot

def create_scatterplot(df):
    # Create a new dataset that includes the data for each country and year
    df_new = pd.DataFrame(columns=['Year', 'Access to electricity'])
    # Loop through the data and extract the data for each country and year
    for country in df['Country'].unique():
        # Extract the data for each country
        df_country = df[df['Country'] == country]
        # Loop through the data for each country and extract the data for each year
        for year in df_country['Year'].unique():
            # Extract the data for each year
            df_year = df_country[df_country['Year'] == year]
            # Extract the access to electricity data
            access_to_electricity = df_year['Access to electricity'].values[0]
            # Append the data to the new dataset
            df_new = df_new.append({'Year': year, 'Access to electricity': access_to_electricity}, ignore_index=True)
    # Create the scatterplot
    fig, ax = plt.subplots()
    ax.scatter(df_new['Year'], df_new['Access to electricity'])
    ax.set_xlabel('Year')
    ax.set_ylabel('Access to electricity')
    ax.set_title('Access to electricity over time')
    # Save the scatterplot
    fig.savefig('static/scatterplot.png')

# # Define a function to display the scatterplot

@app.route('/')
def display_scatterplot():
    # Get the data from the API
    data = get_data()
    # Format the data
    df = format_data(data)
    # Create the scatterplot
    create_scatterplot(df)
    # Display the scatterplot
    return render_template('scatterplot.html')

# # Run the app

if __name__ == '__main__':
    app.run(debug=True)

# Path: templates/scatterplot.html
# Copy code
# <!DOCTYPE html>
# <html>
# <head>
# <title>Access to electricity over time</title>
# </head>
# <body>
# <img src="{{ url_for('static', filename='scatterplot.png') }}" alt="Scatterplot">
# </body>
# </html>


# import matplotlib.pyplot as plt

# # Set the data for the scatterplot
# x = [1, 2, 3, 4, 5]
# y = [1, 4, 9, 16, 25]

# # Create the scatterplot
# fig, ax = plt.subplots()
# ax.scatter(x, y)
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_title('Scatterplot')

# # Save the scatterplot
# fig.savefig('scatterplot.png')
