# KovkMolk Telegram Bot

The KovkMolk Telegram Bot is perfect example of how to overcomplicate a simple telegram bot. It's mostly a joke project but in general, this bot automates the process of tracking and responding to a certain keyword in Telegram group chats. Additionally, it generates and posts a data-driven, XKCD-style chart using weather station data, just because it can and it was fun to explore the possibilities.

## Description

This bot is designed to monitor multiple paragliding club group chats on Telegram and respond when certain keywords are met. Specifically, the bot tracks the last time the word "[Kovk](https://www.kovk-drustvo.si/en/)" or any of its possible typos was mentioned in any of the groups. If this word is mentioned within a certain time frame, the bot breaks the silence and posts a message in one specific group chat. After that, the bot goes to sleep for 1 hour but continues to listen for the keyword to track the last time it was mentioned. The bot also generates a chart based on data from a weather station API and attaches it to the message, adding comments if certain conditions are met.

## Files

1. `KovkMolk.py`: This is the main bot script. It monitors the group chats, tracks the last time the word "Kovk" was mentioned, and sends messages when necessary.

2. `kovkXKCD.py`: This script generates a chart using data from a weather station API. It pulls the data, processes it, and generates a chart. The chart includes comments based on certain conditions defined in the `conditions.py` file. The conditions are chosen randomly from a set of comments stored in the `comments.json` file.

![Chart example](https://cdn.nostr.build/i/fe84b7c5289a58b11578cf14d1400e0ad5434e43c8eda1c183de752e6ff9d6fd.png)

3. `conditions.py`: This script outlines the conditions for adding comments to the chart. These conditions are based on the data retrieved from the weather station API. They include checks for temperature drops, wind speed increases, and wind direction. If these conditions are met, a comment is selected from `comments.json` and added to the chart.

4. `comments.json`: This file contains potential comments that can be added to the chart. These comments are chosen randomly when the conditions in `conditions.py` are met.

5. `last_mention.json`: This file tracks the last time the word "Kovk" or its variations were mentioned in the group chats.

6. `longest_duration.json`, `longest_silence_breaker.json`, `longest_silence_end.json`, `longest_silence_start.json`, `old_longest_silence_breaker.json`: These files are used to track information about the longest silence period. They store the duration of the longest silence, the person who broke the silence, the start and end of the silence period, and the previous record holder, respectively.

7. `bot.log` and `parser.log`: These files are generated automatically after the first run of the `KovkMolk.py` script and are used for logging. `bot.log` logs events related to the Telegram bot, while `parser.log` logs events related to data parsing from the weather station API.

8. `kovkXKCD_4_testing.py` is a chart and comments testing script where we manually set the data parameters.




## Setup & Usage

Before using KovkMolk Telegram Bot, ensure that you have Python 3 installed on your machine. You can download Python 3 from the official [Python website](https://www.python.org/downloads/).

To install the necessary dependencies, navigate to the project directory in your terminal and run the following command:

```
pip install -r requirements.txt
```

This command installs the Python libraries that the bot requires to function correctly.

You need to set up a `.env` file in the project directory to store your sensitive data. This file should contain your Telegram bot token, and the IDs of the group chats the bot is going to monitor. Here is a template of how the `.env` file should look:

```
TELEGRAM_TOKEN=<Your_Telegram_Bot_Token>
SILENT_GROUP_CHAT_ID=<ID_of_the_group_chat_where_the_bot_should_be_silent>
MAIN_GROUP_CHAT_ID=<ID_of_the_group_chat_that_the_bot_also_monitors_and_respond_to>

```

To start the bot, use the following command in the terminal:

```
python KovkMolk.py
```

The bot will now start monitoring the Telegram group chats. It will track when the word "Kovk" or its variations is mentioned in the main group chat. If the conditions are met, it will respond in the main group chat, but it will remain silent in the specified silent group chat.

You can configure the bot's behavior by modifying the `conditions.py` and `comments.json` files.

- `conditions.py`: Defines the conditions under which the bot will add comments to the chart. These conditions are based on the data retrieved from the weather station API. 

- `comments.json`: Contains potential comments that can be added to the chart. The bot will randomly select a comment when the conditions are met.

For any further customization, you can modify the `KovkMolk.py` and `kovkXKCD.py` scripts according to your needs.

For debugging and tracking the bot's activities, check the `bot.log` and `parser.log` files. They provide detailed information about the bot's operation and data parsing events. 

Enjoy using the KovkMolk Telegram Bot!


## HelperScripts

`whenWord.py`, analyses an exported chat log from a Telegram group and provides some statistics based on the occurrence of certain keywords. It calculates:

- The longest duration (silence) between messages containing any of the keywords
- Who broke the silence
- The last time each keyword was mentioned in the chat

The keywords to look for are specified in a list at the start of the script. The script reads multiple HTML files that contain the chat logs, and for each message, it checks whether the message text contains any of the keywords (considering various punctuation marks). The script is case insensitive, meaning it treats 'kovk' and 'KovK' as the same keyword.

The script saves the timestamps and authors of the messages containing the keywords. It sorts these timestamps, calculates the time difference between consecutive timestamps (silences), and identifies the longest silence. It also keeps track of the most recent mention of each keyword.

To use this script, you need to replace `'helperScripts/messages.html'` etc. with the paths to your actual HTML files containing the exported chat logs. Make sure to update the list of keywords if you want to search for different terms.

## Exporting Messages from Telegram group in which you are admin


1. Open the Telegram app on your desktop.
2. Navigate to the chat or group you want to export.
3. Click on the three-dot menu icon in the top right corner.
4. Select 'Export chat history'.
5. You will be prompted to choose the format for the export. Select 'HTML' for compatibility with this script.
6. Click 'Export' to start the process.

**Note:** You'll need to be an Admin of the Telegram group from which you want to export the chat history


`deletePNGs.py`, is designed to delete all PNG files within a specified directory. This could be helpful in situations where you regularly generate PNG files for temporary use (for example, in data analysis or image processing tasks) and want to clean up these temporary files automatically. In our case are the chart images we generate.

Here's how it works:

- The directory containing the PNG files to be deleted is specified in the `somethingSomethingDirectory` variable (in this case, it's set to 'png/').
- The function `delete_png_files()` uses the `glob` module to find all files in the specified directory that match the pattern '*.png'.
- It then iterates over each matched file:
  - It tries to delete the file using the `os.remove()` function.
  - If successful, it prints a message indicating that the file was deleted.
  - If it encounters an error (for example, if the file is open in another program and can't be deleted), it prints an error message.
- Finally, the `delete_png_files()` function is called to execute the PNG deletion process.

## Scheduling the Script

The script can be set up to run automatically at a specific time each day, such as 03:33. This can be achieved using a scheduler such as cron on Unix-based systems or Task Scheduler on Windows.

### Unix-based Systems

For Unix-based systems (like Linux or macOS), you can schedule the script using cron:

1. Open your terminal.
2. Type `crontab -e` to edit the cron table.
3. Add the following line to schedule the script to run at 03:33 every day:

   `33 3 * * * /usr/bin/python3 /path/to/your/script.py`

   Replace '/path/to/your/script.py' with the path to your Python script.

### Windows

On a Windows system, you can use Task Scheduler to achieve the same result:

1. Open Task Scheduler and create a new basic task.
2. Set the trigger to daily at 03:33.
3. Set the action to start a program, which would be your Python script.

Please ensure that the Python environment and the necessary libraries (`os` and `glob`) are correctly set up on the system where the script is scheduled to run.


## Contributing

I appreciate all contributions to improve the KovkMolk Telegram Bot. especially adding new conditions in `conditions.py` or more comments in `comments.json` files 