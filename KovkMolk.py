from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import datetime
import os
import uuid
from dotenv import load_dotenv
import json
import logging
from telegram.error import NetworkError, TelegramError
from kovkXKCD import create_chart  # Import the create_chart function
import time
import warnings
import matplotlib


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.CRITICAL, #level=logging.DEBUG,
    filename='/home/KovkMolk/KovkMolk/bot.log'
)

logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)


load_dotenv()  # load environment variables from .env file
TOKEN = os.getenv("TELEGRAM_TOKEN")  # get token from .env file
SILENT_GROUP_CHAT_ID = int(os.getenv("SILENT_GROUP_CHAT_ID"))  # get silent group chat ID from .env file
MAIN_GROUP_CHAT_ID = int(os.getenv("MAIN_GROUP_CHAT_ID"))  # get main group chat ID from .env file


while True:
    
    try:
        


        # Load the longest duration, last mention, and old breaker from files
        try:
            with open('/home/KovkMolk/KovkMolk/longest_duration.json', 'r') as f:
                longest_duration = datetime.timedelta(seconds=json.load(f))
            with open('/home/KovkMolk/KovkMolk/last_mention.json', 'r') as f:
                last_mention = datetime.datetime.fromisoformat(f.read())
            with open('/home/KovkMolk/KovkMolk/longest_silence_start.json', 'r') as f:
                longest_silence_start = datetime.datetime.fromisoformat(f.read())
            with open('/home/KovkMolk/KovkMolk/longest_silence_end.json', 'r') as f:
                longest_silence_end = datetime.datetime.fromisoformat(f.read())
            with open('/home/KovkMolk/KovkMolk/longest_silence_breaker.json', 'r') as f:
                longest_silence_breaker = f.read()
            with open('/home/KovkMolk/KovkMolk/old_longest_silence_breaker.json', 'r') as f:  # Load the old breaker from a file
                old_longest_silence_breaker = f.read()
        except FileNotFoundError:
            longest_duration = datetime.timedelta()
            last_mention = datetime.datetime.now()
            longest_silence_start = datetime.datetime.now()
            longest_silence_end = datetime.datetime.now()
            longest_silence_breaker = ""
            old_longest_silence_breaker = ""
            
        # To keep track of the last response time
        last_response = datetime.datetime.now() - datetime.timedelta(minutes=1)

        def format_timedelta(td):
            minutes, seconds = divmod(td.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            return f"{td.days} dni, {hours} ur in {minutes} minut"

        def handle_message(update: Update, context: CallbackContext):
            global last_mention
            global last_response
            global longest_duration
            global longest_silence_start
            global longest_silence_end
            global longest_silence_breaker
            global old_longest_silence_breaker
            
            
            now = datetime.datetime.now()
            elapsed_time = now - last_mention
            if elapsed_time < datetime.timedelta(seconds=60):
                # If less than 1 hour has passed since the last mention, do not respond and update the last_mention time
                last_mention = now
                with open('/home/KovkMolk/KovkMolk/last_mention.json', 'w') as f:
                    f.write(now.isoformat())
                return
            
            message = update.effective_message.text.lower() 
            user = update.effective_user.username  # Get the username of the user who sent the message
            

            # Get the bot's username
            bot_username = context.bot.username

            # If the message is from the bot, ignore it
            if user == bot_username:
                return

            forms_of_kovk = ["kovk", "kovku", "kovkom", "kovka", "akovk", "nakovk", "dokovka", "nakovku", 
                                "podkovkom", "zakovkom", "okovk", "kvok", "kovkk", "kov", "kovl", "covk", 
                                "kvoeku", "kovkku", "kovlu", "covku", "kvoekom", "kovkkom", "kobk", "kovlom", "covkom", 
                                "kvoeka", "kovkka", "kovla", "covka", "nakovkk", "nakov", "nakovl", "nacovk", 
                                "dokovkka", "dokovk", "dokovla", "docovka", "nakovkku","konk", "nakovlu", "nacovku", 
                                "podkovkomm", "podkovlom", "podcovkom", "zakovkomm", "zakovlom", "zacovkom", 
                                "kol", "koll", "colk", "kovki", "kovko", "kovke", "nakovki", "nakovko", 
                                "nakovke", "dokovki", "dokovko", "dokovke", "podkovki", "podkovko", "podkovku", 
                                "zakovki", "zakovko", "zakovku", "kovl", "kouk", "kolk", "kovj", "kovm", "kov9", 
                                "kov0", "kovp", "jolk",]
            
            
            # Wait for some time
            time.sleep(5)
            
            if any(form in message for form in forms_of_kovk):
                # now = datetime.datetime.now()
                time_passed = now - last_mention
                formatted_time_passed = format_timedelta(time_passed)  # Format the time passed
                old_longest_duration = longest_duration  # Save the old longest duration
                if time_passed > longest_duration:
                    longest_duration = time_passed
                    longest_silence_start = last_mention  # Set the start of the longest silence to the time of the last mention
                    longest_silence_end = now  # Set the end of the longest silence to the current time
                    old_longest_silence_breaker = longest_silence_breaker  # Save the old breaker
                    longest_silence_breaker = user  # Set the breaker of the longest silence to the current user
                    # Save the new longest duration, silence times, and old breaker to files
                    with open('/home/KovkMolk/KovkMolk/longest_duration.json', 'w') as f:
                        json.dump(longest_duration.total_seconds(), f)
                    with open('/home/KovkMolk/KovkMolk/longest_silence_start.json', 'w') as f:
                        f.write(longest_silence_start.isoformat())
                    with open('/home/KovkMolk/KovkMolk/longest_silence_end.json', 'w') as f:
                        f.write(longest_silence_end.isoformat())
                    with open('/home/KovkMolk/KovkMolk/longest_silence_breaker.json', 'w') as f:
                        f.write(longest_silence_breaker)
                    with open('/home/KovkMolk/KovkMolk/old_longest_silence_breaker.json', 'w') as f:  # Save the old breaker to a file
                        f.write(old_longest_silence_breaker)      

                    # Comment if the record was broken
                    context.bot.send_message(chat_id=MAIN_GROUP_CHAT_ID, text=f"Minilo je natanko {formatted_time_passed} od zadnje omembe Kovka. Kar pomeni, da ste Kovk molk presegli za \
{format_timedelta(longest_duration - old_longest_duration)} in tako zasedli mesto, ki si ga je poprej lastil @{old_longest_silence_breaker}. Čestitke 🏆 \
\n\n Kovk molk je trajal vse od {longest_silence_start.strftime('%d. %m.%Y %H:%M:%S')} pa do danes \
{longest_silence_end.strftime('%d. %m.%Y %H:%M:%S')} \n\nZa nagrado vam pa narišem aktualne razmere iz Kovka.")
                    
                    # Comment if the record has not been broken
                else:
                    context.bot.send_message(chat_id=MAIN_GROUP_CHAT_ID, text=f"Minilo je {formatted_time_passed} od zadnje omembe Kovka.\n\nKot zanimivost, najdaljši Kovk molk je trajal presenetljivih \
{format_timedelta(old_longest_duration)}, od {longest_silence_start.strftime('%d. %m.%Y %H:%M:%S')} \
pa vse tja do {longest_silence_end.strftime('%d. %m.%Y %H:%M:%S')}, ko je {longest_silence_breaker} \
nevede presekal/a Kovk molk \n\nKer smo pa ravno pri Kovku vam narišem trenutne razmere od tam")

                # Create a chart and send it as a photo
                chart_filename = create_chart()
                time.sleep(5)
                with open(f'{chart_filename}.png', 'rb') as file:
                    context.bot.send_photo(chat_id=MAIN_GROUP_CHAT_ID, photo=file)



            last_mention = now  # Update the last mention after checking if the silence was the longest
            # Save the new last mention to a file
            with open('/home/KovkMolk/KovkMolk/last_mention.json', 'w') as f:
                f.write(now.isoformat())


        def main():
            updater = Updater(token=TOKEN, use_context=True)

            dispatcher = updater.dispatcher

            dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))
            
            updater.start_polling()

            updater.idle()

        if __name__ == '__main__':
            main()
            
        pass
    
    except NetworkError as e:
        logger.error(f"Network error: {e}")

    except TelegramError as e:
        logger.critical(f"Telegram error: {e}") 
