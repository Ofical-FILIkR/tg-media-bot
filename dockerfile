from python:3.12

COPY . ./app

RUN python pip install -r requirements.txt

CMD ["python", "run", "create_db_users.py"]
CMD ["python", "run", "bot.py"]