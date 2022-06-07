#!/usr/bin/env python
from telegram_bot import telegram_bot as tb
import os
import time
import logging
import glob
import random
import schedule

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s (%(name)s)', level=logging.INFO)
logger = logging.getLogger(__name__)

class CppTrainingBot(tb.TelegramBot):
    # Constructor
    def __init__(self, user_id, bot_token):
        super().__init__(user_id, bot_token)
        self.active = False
        self.study_cards =  []
        self.study_cards_dir = os.getenv('STUDY_CARDS_DIR')

        self.help_text = "**C++ Training Bot** \nSends study cards about C++ periodically to help with training.\nUse `/switch on` command to enable the bot. For more commands check the command menu."

        self.refresh_study_cards_()
        self.add_command("change", self.cmd_change_directory)
        self.add_command("switch", self.cmd_switch)
        self.add_command("help", self.cmd_help)
        self.add_command("random", self.cmd_get_random_card)

        self.send_msg(self.help_text)

    # Private Functions
    def send_document_(self, file_path, dst=None):
        if dst == None:
            dst = self.user_id
        with open (file_path, 'rb') as fp:
            self.bot.send_document(dst, fp)

    def refresh_study_cards_(self):
        logger.info("Study card list refreshed.")
        self.study_cards = glob.glob(self.study_cards_dir + '/*.*')

    def change_study_cards_directory_(self, new_path):
        self.study_cards_dir = new_path

    # Public Functions
    def send_random_card(self):
        if not self.active:
            return
        if len(self.study_cards) == 0:
            self.refresh_study_cards_()
            if len(self.study_cards) == 0:
                self.send_msg("Instead of a random study card, here is a placeholder text.")
                return
        chosen = random.choice(self.study_cards)
        self.send_document_(chosen)
        self.study_cards.remove(chosen)

    # Bot commands available to user
    #TODO add @tb.restricted decorator, it needs restricted wrap to become a part of original bot and take self as first argument.
    def cmd_help(self, update, context):
        """ Prints the help text """
        self.send_msg(self.help_text)

    def cmd_change_directory(self, update, context):
        """ Take first argument as the new study card directory """
        self.change_study_cards_directory_(context.args[0])

    def cmd_switch(self, update, context):
        """ Takes on or off as argument to stop/start sending cards. """
        if (context.args[0] == 'on'):
            self.active = True
            logger.warning("Training switched ON by the user.")
            self.send_msg("Training switched ON.")
        elif (context.args[0] == 'off'):
            self.active = False
            logger.warning("Training switched OFF by the user.")
            self.send_msg("Training switched OFF.")

    def cmd_get_random_card(self, update, context):
        """ Ask for a random study card, it will be removed from the rotation until refresh."""
        if not self.active:
            self.send_msg("Switch training ON first.")
            return
        self.send_random_card()

def run():
    user_id = os.getenv('TELEGRAM_USER_ID')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = CppTrainingBot(user_id, bot_token)
    bot.start()

    schedule.every().day.at("12:30").do(bot.send_random_card)
    schedule.every().day.at("19:00").do(bot.send_random_card)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run()


