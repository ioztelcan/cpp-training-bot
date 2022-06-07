#!/usr/bin/env python
from telegram_bot import telegram_bot as tb
import os
import time
import logging
import glob
import random

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s (%(name)s)', level=logging.INFO)
logger = logging.getLogger(__name__)

class CppTrainingBot(tb.TelegramBot):
    # Constructor
    def __init__(self, user_id, bot_token):
        super().__init__(user_id, bot_token)
        self.active = False
        self.study_cards =  []
        self.study_cards_dir = os.getenv('STUDY_CARDS_DIR')
        self.refresh_study_cards_()
        self.add_command("change", self.cmd_change_directory)
        self.add_command("switch", self.cmd_switch)

    # Private Functions
    def send_document_(self, file_path, dst=None):
        if dst == None:
            dst = self.user_id
        with open (file_path, 'rb') as fp:
            self.bot.send_document(dst, fp)

    def refresh_study_cards_(self):
        self.study_cards = glob.glob(self.study_cards_dir + '/*.*')

    def change_study_cards_directory_(self, new_path):
        self.study_cards_dir = new_path

    # Public Functions
    def send_random_card(self):
        if not self.active:
            return
        chosen = random.choice(self.study_cards)
        #self.send_document_(chosen)
        self.send_msg("Instead of a random study card, here is a placeholder text.")
        self.study_cards.remove(chosen)
        if len(self.study_cards) == 0:
            self.refresh_study_cards_()

    # Bot commands available to user
    #TODO add @tb.restricted decorator, it needs restricted wrap to become a part of original bot and take self as first argument.
    def cmd_change_directory(self, update, context):
        """ Take first argument as the new study card directory """
        self.change_study_cards_directory_(context.args[0])

    def cmd_switch(self, update, context):
        """ Takes on or off as argument to stop/start sending cards. """
        if (context.args[0] == 'on'):
            self.active = True
            logger.warning("Training switched ON by the user.")
            update.message.reply_text("Training switched ON.")
        elif (context.args[0] == 'off'):
            self.active = False
            logger.warning("Training switched OFF by the user.")
            update.message.reply_text("Training switched OFF.")

# Bot commands
@tb.restricted
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help message comes here')

@tb.restricted
def ping(update, context):
    """Send a pong back."""
    update.message.reply_text('pong')

def run():
    user_id = os.getenv('TELEGRAM_USER_ID')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')


    bot = CppTrainingBot(user_id, bot_token)

    bot.add_command("help", help)
    bot.add_command("ping", ping)

    logger.info("Starting cpp-training-bot")
    bot.start()
    while True:
        bot.send_random_card()
        time.sleep(10)
    #bot.send_msg("C++ training bot online!")



if __name__ == "__main__":
    run()


