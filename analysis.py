# Import flask and pandas libraries
from flask import Flask, request, render_template
import pandas as pd

# Create a flask app
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    # Render the home page template
    return render_template('home.html')

# Define a route for the analysis page
@app.route('/analysis', methods=['POST'])
def analysis():
    # Get the file name from the form input
    file_name = request.form['file_name']
    # Read the file as a pandas dataframe
    df = pd.read_csv(file_name)
    # Get the analysis type from the form input
    analysis_type = request.form['analysis_type']
    # Perform the analysis based on the type
    if analysis_type == 'monthly':
        # Group the data by month and calculate the sum of each column
        df = df.groupby('month').sum()
    elif analysis_type == 'yearly':
        # Group the data by year and calculate the sum of each column
        df = df.groupby('year').sum()
    else:
        # Return an error message if the analysis type is invalid
        return 'Invalid analysis type'
    # Render the analysis page template with the dataframe as an argument
    return render_template('analysis.html', data=df.to_html())
