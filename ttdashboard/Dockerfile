FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
ENV DB_ENGINE=postgre
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
VOLUME /code/static
RUN python manage.py collectstatic
CMD ["daphne", "ttdashboard.asgi:application", "-b", "0.0.0.0"]
