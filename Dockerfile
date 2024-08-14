FROM python:3.11.9-slim-bookworm

RUN apt-get update -y

COPY ./ /app

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR ./src

CMD [ "gunicorn", "--workers", "1", "--bind", "0.0.0.0:8080", "app:app" ]