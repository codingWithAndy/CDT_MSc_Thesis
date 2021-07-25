FROM python:3.8.5

RUN pip install flask flask-cors pyrebase 
RUN pip install gunicorn

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app