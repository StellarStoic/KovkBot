import matplotlib.pyplot as plt
import numpy as np
import logging
import json
import random
from conditions import ConditionChecker
from datetime import datetime


# x-axis = time, y-axis = temp  
# Load the comments from the JSON file
with open('comments.json') as f:
    comments = json.load(f)

# Suppress font warnings
logging.getLogger('matplotlib.font_manager').disabled = True

# Time data
time = ['18:51','19:01','19:11','19:21','19:31','19:41','19:51','20:01','20:11','20:21','20:31','20:41','20:51','21:01','21:03','21:13','21:23','21:33']

# Wind speed data
# wind_speed = [9,11,11,11,9,12,2,2,3,4,7,9,11,11,26,40,30,41]
# wind_speed = [20,20,15,20,22,22,27,29,56,60,40,30,25,17,26,24,20,19]
wind_speed = [20,20,15,20,22,22,27,29,56,60,40,30,25,17,26,24,20,19]

# Wind gusts data
wind_gusts = [8.6,8.0,8.2,7.2,6.2,6.6,9,5.6,5.8,5.4,5.6,6.6,5.6,4,5.0,6.4,6.4,6.0]

# Wind direction data
# wind_direction = [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,3,2,2]
wind_direction = [1,2,2,2,1,2,2,3,3,2,2,2,3,2,2,2,2,3]

# Map numbers to cardinal directions
direction_dict = {0: 'NW', 1: 'W', 2: 'SW', 3: 'S', 4: 'SE', 5: 'E', 6: 'NE', 7: 'N'}
wind_direction_labels = [direction_dict.get(item, item) for item in wind_direction]

# Add a small constant to the wind direction values for visualization
wind_direction_visual = [value + 0.1 for value in wind_direction]

# Temperature data
temperature = [4.0,5,9,1,0,0,0,0,-2,1,5,5,5,8.0,8,5,4.0,6.0]

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

# Create a new figure
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
    if max(temperature) < 12:
        ax1.set_ylabel('Temperatura', fontsize='x-small')
    elif min(temperature) > 18:
        ax1.set_ylabel('Temperatura', fontsize='x-small')
    else:
        ax1.set_ylabel('Temperatura', fontsize='x-small', zorder=1)
    ax2.set_ylabel('m/s', fontsize='x-small')
    

    # Save the plot as an image
    plt.savefig('testing_weather_chart_and _comments.png')

    # Close the plot
    plt.close()
