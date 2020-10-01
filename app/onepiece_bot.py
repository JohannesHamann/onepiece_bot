#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater , CommandHandler
import logging
import func 
from dotenv import load_dotenv
import os

load_dotenv()
Bot_token = os.environ.get("API_TOKEN")


# setting up a logging module, to see when and why things don't work as expected
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

# initialize the bot
def main():
    # Updater class continuously fetches new updates from telegram and passes them to Dispatcher class
    updater = Updater(token= Bot_token, use_context=True)
    dispatcher = updater.dispatcher
    # adds the handlers to dispatcher after being initialized by CommandHandler
    dispatcher.add_handler( CommandHandler("scrape", func.scraping_old) )
    dispatcher.add_handler( CommandHandler("stop", func.stop ) )
    dispatcher.add_handler( CommandHandler("hello", func.hello) )
    # start the bot polling for updates
    updater.start_polling() 
    # make it interuptable with ctrl-c
    updater.idle()

if __name__ == "__main__":
    main()