from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import datetime
from time import sleep
import os
import uuid
from dotenv import load_dotenv
import json
import logging
from telegram.error import NetworkError, TelegramError
from kovkXKCD import create_chart, get_data_freshness_message  # Import the create_chart and get_data_freshness_message functions
import warnings
import time
import matplotlib
import traceback

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.CRITICAL, #level=logging.DEBUG,
    filename='/home/bots/KovkMolk/bot.log'
)

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)

load_dotenv('/home/bots/KovkMolk/.env')  # Load environment variables from .env file
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Get token from .env file
SILENT_GROUP_CHAT_ID = int(os.getenv("SILENT_GROUP_CHAT_ID"))  # Get silent group chat ID from .env file
MAIN_GROUP_CHAT_ID = int(os.getenv("MAIN_GROUP_CHAT_ID"))  # Get main group chat ID from .env file

def format_timedelta(td):
    minutes, seconds = divmod(td.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{td.days} dni, {hours} ur in {minutes} minut"

try:
    with open('/home/bots/KovkMolk/last_mentioner.json', 'r') as f:
        last_mentioner = f.read().strip()
    with open('/home/bots/KovkMolk/pre_last_mentioner.json', 'r') as f:
        pre_last_mentioner = f.read().strip()
    with open('/home/bots/KovkMolk/longest_duration.json', 'r') as f:
        longest_duration = datetime.timedelta(seconds=json.load(f))
    with open('/home/bots/KovkMolk/last_mention.json', 'r') as f:
        last_mention = datetime.datetime.fromisoformat(f.read().strip())
    with open('/home/bots/KovkMolk/longest_silence_start.json', 'r') as f:
        longest_silence_start = datetime.datetime.fromisoformat(f.read().strip())
    with open('/home/bots/KovkMolk/longest_silence_end.json', 'r') as f:
        longest_silence_end = datetime.datetime.fromisoformat(f.read().strip())
    with open('/home/bots/KovkMolk/longest_silence_breaker.json', 'r') as f:
        longest_silence_breaker = f.read()
    with open('/home/bots/KovkMolk/old_longest_silence_breaker.json', 'r') as f:
        old_longest_silence_breaker = f.read()
        
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
except IOError as e:
    logger.error(f"I/O error({e.errno}): {e.strerror}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    logger.error(traceback.format_exc())  # This will print the stack trace to your log

def handle_message(update: Update, context: CallbackContext):
    global last_mentioner
    global pre_last_mentioner
    global last_mention
    global longest_duration
    global longest_silence_start
    global longest_silence_end
    global longest_silence_breaker
    global old_longest_silence_breaker

    now = datetime.datetime.now()
    elapsed_time = now - last_mention
    # Calculate the time since the last mention and the last response
    time_since_last_mention = now - last_mention

    message = update.effective_message.text.lower() 
    user = update.effective_user.username  # Get the username of the user who sent the message

    # Get the bot's username
    bot_username = context.bot.username

    # If the message is from the bot, ignore it
    if user == bot_username:
        return

    forms_of_kovk = ["kovk", "kovku", "kovkom", "kovka", "kowk", "nakovk", "dokovka", "nakovku", 
                        "podkovkom", "zakovkom", "okovku","covk", "kovki",
                        "covku", "kvoekom", "kovkkom", "kobk", "kovlom", "covkom", "kwok", 
                        "kvoeka", "kovko", "kovla", "covka", "nakov", "nakovl", "nacovk", "jovk", "kovc", 
                        "kouk"]

    # Wait for some time
    time.sleep(5)
    
    # Initialize with a message
    time_from_latest_station_data = ""

    if any(form in message for form in forms_of_kovk):
        now = datetime.datetime.now()
        time_passed = now - last_mention
        formatted_time_passed = format_timedelta(time_passed)  # Format the time passed
        old_longest_duration = longest_duration  # Save the old longest duration
        last_mention = now # Update the last mention after checking if the silence was the longest
        
        # Shift mentioner values
        pre_last_mentioner = last_mentioner # Save the previous last_mentioner
        last_mentioner = update.message.from_user.username # Update the current last_mentioner
        try:
            with open('/home/bots/KovkMolk/last_mention.json', 'w') as f: # Save the new last mention to a file
                f.write(now.isoformat())
            last_mentioner = user  # Save the username of the user who last mentioned the keyword
            with open('/home/bots/KovkMolk/last_mentioner.json', 'w') as f:  # Save the last mentioner to a file
                f.write(last_mentioner)
            with open('/home/bots/KovkMolk/pre_last_mentioner.json', 'w') as f:  # Save the pre_last mentioner to a file
                f.write(pre_last_mentioner)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except IOError as e:
            logger.error(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(traceback.format_exc())  # This will print the stack trace to your log   
            
    if time_since_last_mention >= datetime.timedelta(minutes=1): # Bot silence period after responding with a message
        
        time_from_latest_station_data = get_data_freshness_message()  # Get the data freshness message
        
        if time_passed > longest_duration:
            longest_silence_start = longest_silence_end  # Move longest_silence end into longest silence start
            longest_duration = time_passed # Update longest_duration
            longest_silence_end = now  # Set the end of the longest silence to the current time
            old_longest_silence_breaker = longest_silence_breaker  # Save the old breaker
            longest_silence_breaker = user  # Set the breaker of the longest silence to the current user
            
            try:
                # Save the new longest duration, silence times, and old breaker to files...
                last_mention = now # Update the last mention after checking if the silence was the longest
                with open('/home/bots/KovkMolk/last_mention.json', 'w') as f: # Save the new last mention to a file
                    f.write(now.isoformat())
                last_mentioner = user  # Save the username of the user who last mentioned the keyword
                with open('/home/bots/KovkMolk/last_mentioner.json', 'w') as f:  # Save the last mentioner to a file
                    f.write(last_mentioner)
                with open('/home/bots/KovkMolk/pre_last_mentioner.json', 'w') as f:  # Save the pre_last mentioner to a file
                    f.write(pre_last_mentioner)
                with open('/home/bots/KovkMolk/longest_duration.json', 'w') as f:
                    json.dump(longest_duration.total_seconds(), f)
                with open('/home/bots/KovkMolk/longest_silence_start.json', 'w') as f:
                    f.write(longest_silence_start.isoformat())
                with open('/home/bots/KovkMolk/longest_silence_end.json', 'w') as f:
                    f.write(longest_silence_end.isoformat())
                with open('/home/bots/KovkMolk/longest_silence_breaker.json', 'w') as f:
                    f.write(longest_silence_breaker)
                with open('/home/bots/KovkMolk/old_longest_silence_breaker.json', 'w') as f:  # Save the old breaker to a file
                    f.write(old_longest_silence_breaker)     
            except FileNotFoundError as e:
                logger.error(f"File not found: {e}")
            except IOError as e:
                logger.error(f"I/O error({e.errno}): {e.strerror}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                logger.error(traceback.format_exc())  # This will print the stack trace to your log    

            
            # Comment if the record was broken
            context.bot.send_message(chat_id=MAIN_GROUP_CHAT_ID, text=f"Minilo je natanko {formatted_time_passed} odkar je tisti nekdo nazadnje presekal/a Kovk molk. Sedaj je pa točno ta nekdo presegel Kovk molk rekord, za \
{format_timedelta(longest_duration - old_longest_duration)} in tako zasedel mesto, ki si ga je poprej lastil nekdo drug kot Zisti Nekdo. Čestitke za ta nepomemben dosežek 🏆 \
\n\nKovk molk je trajal vse od {longest_silence_start.strftime('%d. %m.%Y %H:%M:%S')} pa do danes \
{longest_silence_end.strftime('%d. %m.%Y %H:%M:%S')}")

            # Comment if the record has not been broken
        else:
            context.bot.send_message(chat_id=MAIN_GROUP_CHAT_ID, text=f"Minilo je točno {formatted_time_passed} od zadnje omembe Kovka.\n\nKot zanimivost, najdaljši Kovk molk je trajal presenetljivih \
{format_timedelta(old_longest_duration)}, od {longest_silence_start.strftime('%d. %m.%Y %H:%M:%S')} \
pa vse tja do {longest_silence_end.strftime('%d. %m.%Y %H:%M:%S')}, ko je Tisti Nekdo \
nevede presekal/a Kovk molk.")

        # Create a chart and send it as a photo
        chart_filename = create_chart()
        time.sleep(3)
        try:
            with open(f'/home/bots/KovkMolk/png/{chart_filename}.png', 'rb') as file:
                context.bot.send_photo(chat_id=MAIN_GROUP_CHAT_ID, photo=file)
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except IOError as e:
            logger.error(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(traceback.format_exc())

        # Add a message about the data freshness after posting the chart image
        context.bot.send_message(chat_id=MAIN_GROUP_CHAT_ID, text=f"Zadnji podatki iz VP Kovk so bili osveženi pred {time_from_latest_station_data}")

def main():
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
