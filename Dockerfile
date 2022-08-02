FROM python:3.10
RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt
RUN pip install python-dotenv
RUN pip install PyDictionary --use-deprecated=backtrack-on-build-failures
RUN pip install py-cord==2.0.0rc1
RUN pip install PyMultiDictionary
COPY . .
USER 1000
CMD [ "python3", "bot.py" ]