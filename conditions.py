import random
from matplotlib.patches import ConnectionStyle

class ConditionChecker:
    def __init__(self, wind_speed, temperature, wind_direction, comments, wind_gusts, colors, ax1, ax2):
        self.wind_speed = wind_speed
        self.temperature = temperature
        self.wind_direction = wind_direction
        self.comments = comments
        self.wind_gusts = wind_gusts
        self.colors = colors
        self.ax1 = ax1
        self.ax2 = ax2

    # check_wind_speed_increase: The loop breaks after adding the first comment when the wind speed increases by more than 10 m/s over two time intervals.
    # Method to check for a gradual increase in wind speed over a certain period of time
    def check_wind_speed_increase(self):
        # Iterate over the wind speed data, starting from the third data point
        for i in range(2, len(self.wind_speed)):
            # Check if the wind speed has increased by more than 10 m/s over two time intervals
            if self.wind_speed[i] - self.wind_speed[i-2] > 10:
                # Select a random comment for wind speed increase
                comment = random.choice(self.comments['wind_speed_increase_in_time'])
                # Format the comment and add it to the plot
                self.format_and_add_comment(comment, i, self.wind_speed[i], self.ax2, 'center', 'right', 'black', 'fancy, head_length=0.4,head_width=0.4,tail_width=0.4', 30, 0.5, (0.1, 0.5), zorder=4)
                return True
        return False


    # check_wrong_wind_direction: The loop breaks after adding the first comment when the last five wind direction bars are in the red unflyable zone, and previous ones are in the green zone.
    def check_wrong_wind_direction(self):
        unflyable_zone = 'red'
        flyable_zone = 'green'
        last_bars = 5  # Set the number of last bars to check

        # Check if there are enough bars
        if len(self.colors) < last_bars + 1:
            return False

        # Check if the last bars are in the unflyable zone
        for i in range(len(self.colors)-1, len(self.colors)-last_bars-1, -1):
            if self.colors[i] != unflyable_zone:
                return False

        # Check if the previous bar is in the flyable zone
        if self.colors[len(self.colors)-last_bars-1] != flyable_zone:
            return False

        # If the last bars are in the unflyable zone and the previous one is in the flyable zone
        # Select a random comment for wrong wind direction
        comment = random.choice(self.comments['wrong_wind_direction'])
        # Format the comment and add it to the plot
        self.format_and_add_comment(comment, i, self.wind_direction[i], self.ax2, 'center', 'right', 'black', None, 40, 1, (0.9, 0.2), 200)
        return True


    #check_constant_wind_direction: The loop breaks after adding the first comment when the wind direction is constant over a certain period of time.
    # Method to check if the wind direction is constant over a certain period of time
    def check_constant_wind_direction(self):
        constant_period = 17  # Set the period for checking constant wind direction
        # Iterate over the wind direction data, starting from the constant_period-th data point
        for i in range(constant_period, len(self.wind_direction)):
            # Check if all values in the period are the same
            if len(set(self.wind_direction[i-constant_period:i])) == 1:
                # Select a random comment for constant wind direction
                comment = random.choice(self.comments['constant_wind_direction'])
                # Format the comment and add it to the plot
                self.format_and_add_comment(comment, i, self.wind_direction[i], self.ax2, 'center', 'center', 'dimgray', None, 30, 0.5, (0.5, 0.2), zorder=200)
                return True
        return False
            
            
    # check_temperature_increase_33: The loop breaks after adding the first comment when the temperature rises above a certain threshold.
    # Method to check if the temperature rises above a certain threshold
    def check_temperature_increase_33(self):
        threshold = 33.0  # Set the temperature threshold
        # Iterate over the temperature data
        for i, temp in enumerate(self.temperature):
            # Check if the temperature is above the threshold
            if temp > threshold:
                # Select a random comment for temperature increase
                comment = random.choice(self.comments['temperature_increase_33'])
                # Format the comment and add it to the plot
                self.format_and_add_comment(comment, i, self.temperature[i], self.ax2, 'center', 'right', 'black',None, 40, 1, (0.1, 0.1), 200)
                # self.format_and_add_comment(comment, i, 0.5, self.ax1, 'center', 'right', 'black', '->', 40, 1, (0.9, 0.5), zorder=200)
                # Add a star marker to the temperature data point
                self.ax1.plot(i, temp, marker='*', color='gold', markersize=10, zorder=200 )
                return True
        return False
            
    
    # check_right_wind_direction: The loop breaks after adding the first comment when the last 3 wind direction bars are in the green flyable zone, and previous ones are in the red zone.
    def check_right_wind_direction(self):
        flyable_zone = 'green' 
        unflyable_zone = 'red'
        last_bars = 3  # Set the number of last bars to check

        # Check if there are enough bars
        if len(self.colors) < last_bars + 1:
            return False

        # Check if the last bars are in the flyable zone
        for i in range(len(self.colors)-1, len(self.colors)-last_bars-1, -1):
            if self.colors[i] != flyable_zone:
                return False

        # Check if the previous bar is in the unflyable zone
        if self.colors[len(self.colors)-last_bars-1] != unflyable_zone:
            return False

        # If the last bars are in the flyable zone and the previous one is in the unflyable zone
        # Select a random comment for right wind direction
        comment = random.choice(self.comments['right_wind_direction'])
        # Format the comment and add it to the plot
        self.format_and_add_comment(comment, i, self.wind_direction[i], self.ax2, 'center', 'right', 'black', None, 40, 1, (0.7, 0.1), 200)
        return True


    # check_wind_speed_range_14_100: The loop breaks after adding the first comment when the wind speed is in the range of 9 - 12 m/s and wind gusts are below 12 m/s for a certain number of points.
    # Method to check if the wind speed is in the range of 14 - 100 m/s and wind gusts are below 12 m/s for a certain number of points
    def check_wind_speed_range_14_100(self, num_points=13):
        lower_wind_speed_limit = 14
        upper_wind_speed_limit = 100
        counter = 0  # Initialize a counter
        # Iterate over the wind speed and wind gusts data
        for i, (speed, gust) in enumerate(zip(self.wind_speed, self.wind_gusts)):
            # Check if wind speed and wind gusts are in range
            if lower_wind_speed_limit <= speed <= upper_wind_speed_limit and gust <= upper_wind_speed_limit:
                counter += 1  # Increment the counter
                # If the condition persists for num_points
                if counter >= num_points:
                    # Select a random comment for wind speed in range
                    comment = random.choice(self.comments['wind_speed_range_14_100'])
                    # Format the comment and add it to the plot
                    self.format_and_add_comment(comment, i, self.wind_speed[i], self.ax2, 'center', 'right', 'black', 'fancy, head_length=0.8, head_width=0.6', 20, 0.05, (0.7, 0.9), zorder=200)
                    return True
            else:
                counter = 0  # Reset the counter if wind speed is out of range


    # check_constant_wind_speed_range_0_2: The loop breaks after adding the first comment when the wind speed is constant in the range of 0 - 2 m/s for a certain number of points.
    # Method to check if the wind speed is constant in the range of 0 - 2 m/s for a certain number of points
    def check_constant_wind_speed_range_0_2(self, num_points=9):
        lower_wind_speed_limit = 0
        upper_wind_speed_limit = 2
        counter = 0  # Initialize a counter
        # Iterate over the wind speed data
        for i, speed in enumerate(self.wind_speed):
            # Check if the wind speed is in the desired range
            if lower_wind_speed_limit <= speed <= upper_wind_speed_limit:
                counter += 1  # Increment the counter
                # If the counter reaches the desired number of points, add a comment
                if counter == num_points:
                    # Select a random comment for constant wind speed in range
                    comment = random.choice(self.comments['constant_wind_speed_range_0_2'])
                    # Format the comment and add it to the plot
                    self.format_and_add_comment(comment, i, self.wind_speed[i], self.ax2, 'center', 'right', 'dimgray', None, 40, 1, (0.1, 0.4), zorder=200)
                    return True  
            else:
                counter = 0  # Reset the counter if the wind speed is out of range


    # check_variable_wind_direction: The loop breaks after adding the first comment when the wind direction is not constant over a certain period of time.
    # Method to check if the wind direction is not constant over a certain period of time
    def check_variable_wind_direction(self):
        variable_period = 16  # Set the period for checking variable wind direction
        # Iterate over the wind direction data, starting from the variable_period-th data point
        for i in range(variable_period, len(self.wind_direction)):
            # Check if all values in the period are different
            if len(set(self.wind_direction[i-variable_period:i])) > 5:
                # Select a random comment for variable wind direction
                comment = random.choice(self.comments['variable_wind_direction'])
                # Format the comment and add it to the plot
                self.format_and_add_comment(comment, i, self.wind_direction[i], self.ax2, 'center', 'center', 'dimgray', None, 60, 1, (0.5, 0.2), zorder=200)
                return True
        return False


    # check_persistent_low_temperature: The loop breaks after adding the first comment when the temperature is below zero for a certain period of time.
    # Method to check if the temperature is below zero for a certain period of time
    def check_persistent_low_temperature(self, period=5):
        count = 0  # Initialize a counter
        # Iterate over the temperature data
        for i, temp in enumerate(self.temperature):
            # Check if the temperature is below zero
            if temp < -5:
                count += 1  # Increment the counter
                # If the temperature is below zero for a certain period of time, add a comment
                if count >= period:
                    # Select a random comment for persistent low temperature
                    comment = random.choice(self.comments['persistent_low_temperature'])
                    # Format the comment and add it to the plot
                    # self.format_and_add_comment(comment, i, 0.5, self.ax1, 'center', 'right', 'black', '->', 40, 1, (0.9, 0.5), zorder=200)
                    self.format_and_add_comment(comment, i, self.temperature[i], self.ax2, 'center', 'right', 'black',None, 40, 1, (0.1, 0.1), 200)
                    # Add a star marker to the temperature data point
                    self.ax1.plot(i, temp, marker='*', color='gold', markersize=10, zorder=200 )
                    return True
            else:
                count = 0  # Reset the counter if the temperature is above zero


    def check_wind_speed_range_5_8(self, num_points=16):
        lower_wind_speed_limit = 5
        upper_wind_speed_limit = 9
        green_counter = 0  # Initialize a counter for green points
        # Iterate over the wind speed data
        for i, speed in enumerate(self.wind_speed):
            # Get the color at the current point
            color = self.colors[i]
            # Check if wind speed is in range and color is green
            if lower_wind_speed_limit <= speed <= upper_wind_speed_limit and color == 'green':
                green_counter += 1  # Increment the green counter
            elif color == 'red':
                green_counter = 0  # Reset the green counter if color is red
            # If wind speed is out of range, break the loop and conditions are not met
            if not lower_wind_speed_limit <= speed <= upper_wind_speed_limit:
                return True
        # If the condition persists for num_points and last 9 points are green
        if i == len(self.wind_speed) - 1 and green_counter >= 9:
            # Select a random comment for wind speed in range
            comment = random.choice(self.comments['wind_speed_range_5_8'])
            # Format the comment and add it to the plot
            self.format_and_add_comment(comment, i, self.wind_speed[i], self.ax2, 'center', 'right', 'dimgray', '->', 40, 0.8, (0.4, 0.5), zorder=200)
            return True
        return False
    
    def format_and_add_comment(self, comment, x, y, ax, va, ha, color, arrowstyle, shrinkA, shrinkB, xytext, zorder):
        """
        Method to format the comment and add it to the plot.

        Parameters:
        comment (str): The comment to be added.
        x (int): The x-coordinate of the point of interest.
        y (int): The y-coordinate of the point of interest.
        ax (matplotlib.axes.Axes): The axes to which the comment should be added.
        va (str): The vertical alignment of the comment.
        ha (str): The horizontal alignment of the comment.
        color (str): The color of the comment.
        arrowstyle (str): The style of the arrow pointing to the point of interest.
        shrinkA (float): The fraction of the arrow length by which the arrow is shrunk from the A point.
        shrinkB (float): The fraction of the arrow length by which the arrow is shrunk from the B point.
        xytext (tuple): The position (x, y) to place the text at.
        zorder (int): The layer order for the comment in the plot.
        """
        # Break the comment into words
        words = comment.split()

        # Group the words into lines of 3-4 words
        lines = [' '.join(words[i:i+3]) for i in range(0, len(words), 3)]

        # Join the lines with newline characters
        multiline_comment = '\n'.join(lines)

        # Create an arrow annotation if arrowstyle is not None
        arrowprops = None
        if arrowstyle is not None:
            arrowprops = dict(arrowstyle=arrowstyle, color=color, shrinkA=shrinkA, shrinkB=shrinkB, connectionstyle='arc3,rad=0.4', mutation_scale=20)

        # Ensure the xytext coordinates do not escape the plot
        xytext = (max(0, min(1, xytext[0])), max(0, min(1, xytext[1])))
        
        # Choose a random rotation angle between -40 and +40 degrees
        rotation_angle = random.randint(-40, 40)

        # Add the comment to the plot with the random rotation angle
        ax.annotate(multiline_comment, (x, y), xytext=xytext, textcoords='axes fraction', va=va, ha='center', 
                    arrowprops=arrowprops, zorder=zorder, fontsize='small', rotation=rotation_angle)            
    
    def check_conditions(self):
        # List of condition methods
        conditions = [
            self.check_wind_speed_increase,
            self.check_wrong_wind_direction,
            self.check_constant_wind_direction,
            self.check_temperature_increase_33,
            self.check_right_wind_direction,
            self.check_wind_speed_range_14_100,
            self.check_constant_wind_speed_range_0_2,
            self.check_variable_wind_direction,
            self.check_persistent_low_temperature,
            self.check_wind_speed_range_5_8
        ]
        
        # Shuffle the conditions to randomize the order in which they are checked
        random.shuffle(conditions)

        # Check each condition
        for method in conditions:
            method()
