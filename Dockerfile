FROM python:3.9.6-alpine3.14

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /src/DEALS
WORKDIR /src/DEALS

ADD . /src/DEALS

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python3.9 manage.py makemigrations && python3.9 manage.py migrate

CMD python3.9 manage.py runserver 127.0.0.1:8000
EXPOSE 8000

