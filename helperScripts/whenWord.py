import datetime
import re
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# Custom date parsing function
def parse_date(date_str):
    date_str, time_str, tz_str = date_str.split(" ")
    day, month, year = map(int, date_str.split('.'))
    hour, minute, second = map(int, time_str.split(':'))
    dt = datetime(year, month, day, hour, minute, second)
    if '+' in tz_str:
        tz_hour, tz_minute = map(int, tz_str.split("+")[1].split(":"))
        tzinfo = timezone(timedelta(hours=tz_hour, minutes=tz_minute))
    elif '-' in tz_str:
        tz_hour, tz_minute = map(int, tz_str.split("-")[1].split(":"))
        tzinfo = timezone(-timedelta(hours=tz_hour, minutes=tz_minute))
    else:  # no timezone offset provided
        tzinfo = timezone.utc
    return dt.replace(tzinfo=tzinfo)

# An empty dictionary to hold the most recent timestamp of each keyword
last_mentioned = defaultdict(lambda: (datetime.min.replace(tzinfo=timezone.utc), "Unknown"))

# List of HTML files that you've exported from Telegram
html_files = ['helperScripts/messages.html', 'helperScripts/messages2.html', 'helperScripts/messages3.html', 'helperScripts/messages4.html', 'helperScripts/messages5.html']

# Keywords list
keywords = ["kovk", "kovku", "kovkom", "kovka", "akovk", "nakovk", "dokovka", "nakovku", 
                                "podkovkom", "zakovkom", "okovk", "kvok", "kovkk", "kov", "kovl", "covk", 
                                "kvoeku", "kovkku", "kovlu", "covku", "kvoekom", "kovkkom", "kobk", "kovlom", "covkom", 
                                "kvoeka", "kovkka", "kovla", "covka", "nakovkk", "nakov", "nakovl", "nacovk", 
                                "dokovkka", "dokovk", "dokovla", "docovka", "nakovkku","konk", "nakovlu", "nacovku", 
                                "podkovkomm", "podkovlom", "podcovkom", "zakovkomm", "zakovlom", "zacovkom", 
                                "kol", "koll", "colk", "kovki", "kovko", "kovke", "nakovki", "nakovko", 
                                "nakovke", "dokovki", "dokovko", "dokovke", "podkovki", "podkovko", "podkovku", 
                                "zakovki", "zakovko", "zakovku", "kovl", "kouk", "kolk", "kovj", "kovm", "kov9", 
                                "kov0", "kovp", "jolk",]

# An empty list to hold the timestamps of all messages containing the keywords
timestamps = []

# Same for the usernames
usernames = []

# Loop over each HTML file
for html_file in html_files:
    # Open the file in read mode
    with open(html_file, 'r') as f:
        # Parse the HTML content of the file with BeautifulSoup
        soup = BeautifulSoup(f, 'html.parser')

    # Find all message elements in the HTML
    message_elements = soup.find_all('div', class_='message default clearfix')

    # Loop over each message
    for message in message_elements:
        # Find the timestamp element of the message
        timestamp_element = message.find('div', class_='pull_right date details')
        # Extract the timestamp string from the 'title' attribute of the timestamp element
        timestamp_str = timestamp_element.get('title')
        # Convert the timestamp string to a datetime object
        timestamp = parse_date(timestamp_str)

        # Find the username or full name of the user who sent the message
        user_element = message.find('div', class_='from_name')
        username = user_element.get_text() if user_element else "Unknown"

        # Check if any keyword exists in the message text
        for keyword in keywords:
            pattern = fr'\b{re.escape(keyword)}\b[!?\.,]*'
            if re.search(pattern, message.get_text(), re.IGNORECASE):
                # Add the datetime object and username to their respective lists
                timestamps.append(timestamp)
                usernames.append(username)
                
                # Update the last mentioned time of the keyword if this mention is more recent
                last_time, _ = last_mentioned[keyword]
                if timestamp > last_time:
                    last_mentioned[keyword] = (timestamp, username)

# Ensure the timestamps are in chronological order
timestamps, usernames = zip(*sorted(zip(timestamps, usernames)))

# Calculate the time differences between consecutive timestamps
differences = [(i, j, j-i, u) for i, j, u in zip(timestamps[:-1], timestamps[1:], usernames[1:])]

# Sort the time differences by duration
differences.sort(key=lambda x: x[2])

# The longest silence is the largest time difference
longest_silence = differences[-1] if differences else None

# If there was at least one silence period
if longest_silence:
    # Print the duration of the longest silence
    print(f"Longest silence: {longest_silence[2]}")
    # Print the start time of the longest silence
    print(f"From: {longest_silence[0].strftime('%d.%m.%Y %H:%M:%S')}")
    # Print the end time of the longest silence
    print(f"To: {longest_silence[1].strftime('%d.%m.%Y %H:%M:%S')}")
    # Print the username who broke the silence
    print(f"Broken by: {longest_silence[3]}")
else:
    # If there was no silence period (i.e., the keywords were in every message), print a message saying so
    print("No silence period found")

# Print the last time each keyword was mentioned
for keyword, (timestamp, username) in last_mentioned.items():
    print(f"Keyword '{keyword}' was last mentioned at {timestamp.strftime('%d.%m.%Y %H:%M:%S')} by {username}")
