FROM python:3.8-slim-buster

COPY ./ /etc/xwillmarktheBot

#RUN pip install dash dash_core_components pandas requests

VOLUME ["/etc/xwillmarktheBot/logs", "/etc/xwillmarktheBot/Settings"]

WORKDIR /etc/xwillmarktheBot
CMD ["python", "-m", "xwillmarktheBot.Main", "$platform"]
