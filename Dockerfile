FROM python:3.12.6

WORKDIR /app

COPY . .    

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver"]