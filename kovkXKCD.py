import matplotlib.pyplot as plt
import numpy as np
import logging
import json
import random
import requests
from bs4 import BeautifulSoup
import re
import uuid
import time
from conditions import ConditionChecker
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Create a logger for this module
logger = logging.getLogger('/home/KovkMolk/KovkMolk/kovkXKCD')
logger.setLevel(logging.INFO)

# Create a file handler for this logger
fh = logging.FileHandler('/home/KovkMolk/KovkMolk/parser.log')
fh.setLevel(logging.INFO)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(fh)

# Load the comments from the JSON file
with open('/home/KovkMolk/KovkMolk/comments.json') as f:
    comments = json.load(f)
    
# Suppress font warnings
logging.getLogger('matplotlib.font_manager').disabled = True

# Fetch the KOK_API_KEY from the environment variables
KOK_API_KEY = os.getenv("KOK_API_KEY")

# Parsing the data
while True:
    try:
        # Send a GET request to the URL to fetch the HTML content.
        url = f'https://api.kok.si/widget_app.php?key={KOK_API_KEY}'
        response = requests.get(url)
        # Parse the HTML content with BeautifulSoup.
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the script tags in the HTML.
        scripts = soup.find_all('script')
        # Extract the JavaScript code from the script tags.
        js_code = [script.string for script in scripts if script.string is not None]
        # Use a regular expression to find the data arrays in the JavaScript code.
        data_regex = re.compile(r'data: \[(.*?)\]')
        data_matches = data_regex.findall(' '.join(js_code))
        # Clean up the matches to get just the data arrays.
        data_arrays = [[float(num) for num in match.split(',') if num] for match in data_matches]
        # Use a regular expression to find the time arrays in the JavaScript code.
        time_regex = re.compile(r'categories: \[(.*?)\]')
        time_matches = time_regex.findall(' '.join(js_code))
        # Clean up the matches to get just the time arrays.
        time_arrays = [[time.strip("'") for time in match.split(',')] for match in time_matches]

        # Assign the data arrays to variables.
        temperature = data_arrays[3]
        # Time data
        time = time_arrays[0][:-1]
        # Wind speed data
        wind_speed = data_arrays[0]
        # Wind gusts data
        wind_gusts = data_arrays[1]
        # Wind direction data
        wind_direction = data_arrays[2]

        # Map numbers to cardinal directions
        direction_dict = {0: 'NW', 1: 'W', 2: 'SW', 3: 'S', 4: 'SE', 5: 'E', 6: 'NE', 7: 'N'}
        wind_direction_labels = [direction_dict.get(item, item) for item in wind_direction]

        # Add a small constant to the wind direction values for visualization
        wind_direction_visual = [value + 0.1 for value in wind_direction]

        # # Temperature data
        # temperature = [24.0,23.0,23.0,23.0,22.0,22.0,22.0,21.0,20.0,20.0,19.0,19.0,19.0,18.0,18.0,18.0,18.0,18.0]
        
        # If the scraping is successful, break the loop
        break
    except Exception as e:
            logger.error(f"Unable to scrape data from the API. The error message is: {e}")
            # Optional: add a delay before trying again
            time.sleep(10)  # wait for 60 seconds# END parsing data 

# Define the flyable wind directions
flyable = ['S', 'SW', 'W']
unFlyable = ['N', 'NE', 'NW', 'E', 'SE']
conditionable = []

# Create a list of colors based on the wind direction labels
colors = []
for direction in wind_direction_labels:
    if direction in flyable:
        colors.append('green')
    elif direction in unFlyable:
        colors.append('red')
    elif direction in conditionable:
        colors.append('orange')
    else:
        colors.append('grey')  # default color
        

# Define the upper and lower wind speed limits
lower_limit = 5
upper_limit = 8

def create_chart():
    with plt.xkcd():
        fig, ax1 = plt.subplots()


        # Create a secondary y-axis for the wind direction
        ax2 = ax1.twinx()

        # Initialize the condition checker
        checker = ConditionChecker(wind_speed, temperature, wind_direction, comments, wind_gusts, colors, ax1, ax2)

        # Check conditions
        checker.check_conditions()

        # Add horizontal lines for soaring limits
        ax2.axhline(y=lower_limit, color='green', linestyle='--', zorder=1)
        ax2.axhline(y=upper_limit, color='red', linestyle='--', zorder=1)

        # Fill the space between the soaring limits lines
        ax2.fill_between(time, lower_limit, upper_limit, color='mediumspringgreen', alpha=0.1) 

        # Plot wind direction as a bar chart on the secondary y-axis with the colors
        ax2.bar(time, wind_direction_visual, alpha=0.1, color=colors, label='Wind Direction')
        for i, txt in enumerate(wind_direction_labels):
            ax2.text(i, wind_direction_visual[i], txt, ha='center', va='center', rotation=45, fontsize='x-small', zorder=1)

        # Plot temperature on the primary y-axis
        line1, = ax1.plot(time, temperature, label='Temperatura', color='tab:orange', linestyle='dotted',zorder=1)

        # Plot wind speed on the secondary y-axis
        line2, = ax2.plot(time, wind_speed, label='Hitrost vetra', color='tab:blue', zorder=1)

        # Plot wind gusts on the secondary y-axis
        line3, = ax2.plot(time, wind_gusts, label='Sunki vetra', color='tab:red', linestyle=(0,(5,1)), zorder=1)




        # Define lines here before using it in the loop
        lines = [line1, line2, line3]

        # Add values at the beginning and end of the lines
        for i, line in enumerate(lines):
            # Get the data for the line
            xdata = line.get_xdata()
            ydata = line.get_ydata()

            # Define the offset
            offset = i * 0.4

            # Add text at the beginning of the line if it's unique
            if ydata[0] not in [l.get_ydata()[0] for l in lines if l != line]:
                if ydata[0] < ydata[-1]:
                    if line == line1:
                        ax1.text(xdata[0], ydata[0] + offset, f'{ydata[0]:.1f}', color=line.get_color(), verticalalignment='top', fontsize='x-small')
                    else:
                        ax2.text(xdata[0], ydata[0] + offset, f'{ydata[0]:.1f}', color=line.get_color(), verticalalignment='top', fontsize='x-small')
                else:
                    if line == line1:
                        ax1.text(xdata[0], ydata[0] + offset, f'{ydata[0]:.1f}', color=line.get_color(), verticalalignment='bottom', fontsize='x-small')
                    else:
                        ax2.text(xdata[0], ydata[0] + offset, f'{ydata[0]:.1f}', color=line.get_color(), verticalalignment='bottom', fontsize='x-small')

            # Add text at the end of the line if it's unique
            if ydata[-1] not in [l.get_ydata()[-1] for l in lines if l != line]:
                if ydata[-1] < ydata[0]:
                    if line == line1:
                        ax1.text(xdata[-1], ydata[-1] + offset, f'{ydata[-1]:.1f}', color=line.get_color(), verticalalignment='top', fontsize='x-small')
                    else:
                        ax2.text(xdata[-1], ydata[-1] + offset, f'{ydata[-1]:.1f}', color=line.get_color(), verticalalignment='top', fontsize='x-small')
                else:
                    if line == line1:
                        ax1.text(xdata[-1], ydata[-1] + offset, f'{ydata[-1]:.1f}', color=line.get_color(), verticalalignment='bottom', fontsize='x-small')
                    else:
                        ax2.text(xdata[-1], ydata[-1] + offset, f'{ydata[-1]:.1f}', color=line.get_color(), verticalalignment='bottom', fontsize='x-small')

        # Add a legend
        lines = [line1, line2, line3]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.45, -0.071), ncol=3, fontsize='xx-small')
        # Create custom x-axis labels
        # xticks = [t if ':01' in t or ':00' in t else '' for t in time]
        # ax1.set_xticks(range(len(time)))
        # ax1.set_xticklabels(xticks, fontsize='x-small')
        xticks = [time[0], 'čas', time[-1]]
        ax1.set_xticks([0, len(time)//2, len(time)-1])
        ax1.set_xticklabels(xticks, fontsize='x-small')

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45)

        # Get the current date and time
        now = datetime.now()
        formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')

        # Add a title to the chart
        plt.title(f'Kovk    {formatted_now}', zorder=1)
        
        # Set y-axis labels with units
        if max(temperature) < 12.9:
            ax1.set_ylabel('Temperatura', fontsize='x-small')
        elif min(temperature) > 18:
            ax1.set_ylabel('Temperatura', fontsize='x-small')
        else:
            ax1.set_ylabel('Temperatura', fontsize='x-small', zorder=1)
        ax2.set_ylabel('m/s', fontsize='x-small')
        

        # Save the plot as an image
        filename = '/home/KovkMolk/KovkMolk/png/weather_chart_' + str(uuid.uuid4())
        plt.tight_layout()
        plt.savefig(filename + '.png')

        # Close the plot
        plt.close()

        logger.info("A chart was successfully drawn.")

        def count_charts_drawn(log_file):
            with open(log_file, 'r') as file:
                lines = file.readlines()
            count = sum("A chart was successfully drawn." in line for line in lines)
            return count
        
        charts_drawn = count_charts_drawn("/home/KovkMolk/KovkMolk/parser.log")
        print(f"Total charts drawn: {charts_drawn}")    


        return filename
