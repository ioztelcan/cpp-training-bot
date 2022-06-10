FROM python:3.8-slim-buster

ARG TELEGRAM_USER_ID
ARG TELEGRAM_BOT_TOKEN
#ARG DATA_DIR=$DATA_DIR
ARG TZ

ENV TELEGRAM_USER_ID=$TELEGRAM_USER_ID
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV DATA_DIR="/data"
ENV TZ=$TZ

WORKDIR /app/telegram_bot
COPY telegram_bot .

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY bot.py .

CMD [ "python3", "bot.py"]
