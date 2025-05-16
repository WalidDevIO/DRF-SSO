FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "python", "manage.py", "runserver", "0:8000" ]