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

SOURCE_LIST = {0:"files", 1:"links", 2:"notion"}

class CppTrainingBot(tb.TelegramBot):
    # Constructor
    def __init__(self, user_id, bot_token):
        super().__init__(user_id, bot_token)
        self.active = True
        self.study_cards =  []
        self.data_dir = os.getenv('DATA_DIR')
        self.source = 1 # 0: pull from directory, 1: pull links from a file 2: get from notion directly
        self.source_dir = "{}/links".format(os.getenv('DATA_DIR'))
        self.scheduler = schedule.Scheduler()

        self.help_text = "*C\+\+ Training Bot* \nSends study cards about C\+\+ periodically to help with training\.\nUse \"/switch on\" command to enable the bot\. Available commands: `dir,switch,help,random,status,refresh,source,jobs,schedule,delete,deleteall`\."

        self.refresh_study_cards_()
        self.add_command("dir", self.cmd_set_source_dir)
        self.add_command("switch", self.cmd_switch)
        self.add_command("help", self.cmd_help)
        self.add_command("random", self.cmd_get_random_card)
        self.add_command("status", self.cmd_get_status)
        self.add_command("refresh", self.cmd_force_refresh)
        self.add_command("source", self.cmd_change_source)
        self.add_command("jobs", self.cmd_get_scheduled_jobs)
        self.add_command("delete", self.cmd_delete_job)
        self.add_command("deleteall", self.cmd_delete_all_jobs)
        self.add_command("schedule", self.cmd_schedule_job)

        self.send_msg(self.help_text, parse_mode="MarkdownV2")

    # Private Functions
    def set_source_dir_(self, new_dir):
        """ source 1 actually takes a file not a directory """
        self.source_dir = new_dir

    def send_document_(self, file_path, dst=None):
        with open (file_path, 'rb') as fp:
            self.bot.send_document(dst, fp)

    def send_link_(self, link, dst=None):
        self.send_msg("<a href=\"{link}\">{link}</a>".format(link=link), parse_mode="HTML")

    def send_card_(self, card, dst=None):
        if dst == None:
            dst = self.user_id
        if self.source == 0:
            send = self.send_document_
        elif self.source == 1:
            send = self.send_link_
        send(card, dst)

    def refresh_study_cards_(self):
        self.study_cards.clear()
        if self.source == 0:
            self.study_cards = glob.glob(self.source_dir + '/*.*')
        elif self.source == 1:
            with open (self.source_dir, "r") as link_file:
                for line in link_file:
                    if not line.startswith('#'):
                        self.study_cards.append(line.strip('\n'))
        logger.info("Study card list refreshed.")

    def check_source_(self):
        return self.source

    def change_source_(self, source):
        self.source = source
        if self.source == 0:
            self.source_dir = "{}/cards".format(os.getenv('DATA_DIR'))
        elif self.source == 1:
            self.source_dir = "{}/links".format(os.getenv('DATA_DIR'))
        logger.info("Changed source to: {}".format(SOURCE_LIST[source]))

    # Public Functions
    def send_random_card(self):
        """ Send a random study card. """
        if not self.active:
            return
        if len(self.study_cards) == 0:
            self.refresh_study_cards_()
            print(self.study_cards)
            if len(self.study_cards) == 0:
                self.send_msg("Instead of a random study card, here is a placeholder text.")
                return
        chosen = random.choice(self.study_cards)
        self.send_card_(chosen)
        self.study_cards.remove(chosen)

    def schedule_job(self, time):
        """ Simple function to schedule a send card job at a certain time during day. """
        self.scheduler.every().day.at(time).do(self.send_random_card)

    def delete_job(self, job):
        self.scheduler.cancel_job(job)

    def delete_all_jobs(self):
        self.scheduler.clear()

    def get_scheduled_jobs(self):
        return self.scheduler.get_jobs()


    # Bot commands available to user
    #TODO add @tb.restricted decorator, it needs restricted wrap to become a part of original bot and take self as first argument.
    def cmd_help(self, update, context):
        """ Prints the help text """
        self.send_msg(self.help_text, parse_mode="MarkdownV2")

    def cmd_set_source_dir(self, update, context):
        """ Take first argument as the new study card directory """
        self.set_source_dir_(context.args[0])
        self.refresh_study_cards_()
        self.send_msg("New source dir: *{}*".format(self.source_dir), parse_mode="MarkdownV2")
        logger.warning("Source dir changed to {} by the user.".format(self.source_dir))

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

    def cmd_get_status(self, update, context):
        """ Get status information about configuration etc. """
        msg = "*Active:* `{status}`\n*Source:* `{source}`\n*Directory:* `{directory}`\n*Cards left:* `{cards_left}`\n".format(
        status=self.active,
        source=SOURCE_LIST[self.source],
        directory=self.source_dir,
        cards_left=len(self.study_cards))
        self.send_msg(msg, parse_mode="MarkdownV2")

    def cmd_force_refresh(self, update, context):
        """ Force a card list refresh. """
        self.refresh_study_cards_()
        self.send_msg("Card list refreshed, cards left: *{}*".format(len(self.study_cards)), parse_mode="MarkdownV2")
        logger.warning("User {}({}) forced a card list refresh.".format(update.effective_user.first_name, update.effective_user.id))

    def cmd_change_source(self, update, context):
        if int(context.args[0]) in SOURCE_LIST.keys():
            self.change_source_(int(context.args[0]))
            self.refresh_study_cards_()
            self.send_msg("Source changed to {}, cards left: {}".format(SOURCE_LIST[self.source], len(self.study_cards)))
            logger.warning("Source changed to {}, cards left: {}".format(SOURCE_LIST[self.source], len(self.study_cards)))
        else:
            self.send_msg("Invalid source argument passed.")

    def cmd_get_scheduled_jobs(self, update, context):
        jobs = self.get_scheduled_jobs()
        if len(jobs) == 0:
            self.send_msg("There are no scheduled jobs.")
            return
        cnt = 0
        msg = ""
        for job in jobs:
            msg = msg + "__ID:__ `{}` __Next:__ `{}`\n".format(cnt, job.next_run)
            cnt = cnt + 1
        self.send_msg(msg, parse_mode="MarkdownV2")

    def cmd_schedule_job(self, update, context):
        self.schedule_job(context.args[0])
        self.cmd_get_scheduled_jobs(update, context)

    def cmd_delete_job(self, update, context):
        job_id = int(context.args[0])
        jobs = self.get_scheduled_jobs()
        self.delete_job(jobs[job_id])
        self.cmd_get_scheduled_jobs(update, context)

    def cmd_delete_all_jobs(self, update, context):
        self.delete_all_jobs()
        self.send_msg("Deleted all jobs")

def run():
    user_id = os.getenv('TELEGRAM_USER_ID')
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = CppTrainingBot(user_id, bot_token)
    bot.start()

    bot.schedule_job("12:30")
    bot.schedule_job("19:00")

    while True:
        bot.scheduler.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run()


