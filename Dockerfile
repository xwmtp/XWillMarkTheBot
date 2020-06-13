FROM python:3.8-slim-buster

ENV platform s

COPY ./ /etc/xwillmarktheBot

RUN pip install requests isodate pytz discord

VOLUME ["/etc/xwillmarktheBot/logs", "/etc/xwillmarktheBot/Settings"]

WORKDIR /etc/xwillmarktheBot
CMD ["sh", "-c", "python -m xwillmarktheBot.Main ${platform}"]