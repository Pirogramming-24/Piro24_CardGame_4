FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate --noinput &&\
    python manage.py runserver 0.0.0.0:8000

EXPOSE 8000