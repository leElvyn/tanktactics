FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DB_ENGINE=postgre
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/