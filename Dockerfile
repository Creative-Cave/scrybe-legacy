FROM python:3.9

COPY requirements.txt .

RUN pip freeze > requirements.txt

RUN pip install -r requirements.txt

RUN pip install git+https://github.com/Pycord-Development/pycord

RUN pip install python-dotenv

RUN pip install PyDictionary --use-deprecated=backtrack-on-build-failures

COPY . .

USER 1000

CMD [ "python3", "-B", "Scrybe-2/bot.py" ]
