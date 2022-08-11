# cpp-training-bot

A bot that can send study cards at scheduled times during the day.

- Currently reads links to cards/material and sends them to you at scheduled times of the day.
- Schedule can be configured on the fly through telegram.
- Bot can be switched off or on through telegram interface.
- Dockerized, so it's easy to deploy.

## Usage

Requires Python 3.6 or later. Install requirements using:
`pip install -r requirements.txt`

Add telegram user id (yours), bot token and data directory in env_variables file, then source it:
`source env_variables`

Makefile commands can be used to build or run the container or create an image file. It's also possible to just run it with `./bot.py`

## Commands

- `/switch [on/off]`: Switch training on or off without killing the process.
- `/status`: Sends status information about the bot.
- `/random`: Sends a random study card.
- `/refresh`: Refreshes the card list.
- `/jobs`: Shows scheduled times to send cards.
- `/schedule [HH:MM:SS]`: Schedules a time to send study cards.
- `/delete [job-id]`: Deletes the scheduled job.
- `/deleteall`: Delete all scheduled jobs.
- `/source [0/1/2]`: Can be set to 0 to send files and 1 to send links
- `/dir`: Can be used to change study card source directory.




