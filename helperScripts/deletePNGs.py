# To schedule this script to run at 03:33 every day, you can use a cron job on a Unix-based system. 
# 
# Here's how you can do it:

# Open your terminal.
# Type crontab -e to edit the cron table.
# Add the following line to schedule the script to run at 03:33 every day:
# ruby
# Copy code
# 33 3 * * * /usr/bin/python3 /path/to/your/script.py
# Replace '/path/to/your/script.py' with the path to your Python script.

# This line tells cron to run the script using Python 3 at minute 33 of hour 3 (03:33) every day
# of the month, every month, and every day of the week.

# On a Windows system, you can use Task Scheduler to achieve the same result. 
# You would create a new basic task, set the trigger to daily at 03:33, and the action to start a program,
# which would be your Python script.

import os
import glob

# Specify the directory you want to delete files from
directory = '/home/KovkMolk/KovkMolk/png/'

def delete_png_files():
    # Use glob to match .png file pattern
    files = glob.glob(directory + '/*.png')

    for file in files:
        try:
            # Remove the file
            os.remove(file)
            print(f'Successfully deleted {file}')
        except OSError as e:
            print(f'Error: {file} : {e.strerror}')

# Call the function
delete_png_files()
