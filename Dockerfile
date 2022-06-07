FROM python:3.8-slim-buster

WORKDIR /app/telegram_bot
COPY telegram_bot .

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY bot.py .

CMD [ "python3", "bot.py"]
