#!/usr/bin/env python
from telegram_bot import telegram_bot as tb
import os
import time
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s (%(name)s)', level=logging.INFO)
logger = logging.getLogger(__name__)

class CppTrainingBot(tb.TelegramBot):
    def send_document(self, file_path, dst=None):
        if dst == None:
            dst = self.user_id
        with open (filepath, 'rb') as fp:
            self.bot.send_document(dst, fp)

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
    study_cards_dir = os.getenv('STUDY_CARDS_DIR')

    bot = CppTrainingBot(user_id, bot_token)

    bot.add_command("help", help)
    bot.add_command("ping", ping)

    logger.info("Starting cpp-training-bot")
    bot.start()
    bot.send_msg("C++ training bot online!")

if __name__ == "__main__":
    run()


