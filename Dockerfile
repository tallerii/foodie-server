FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# Allows docker to cache installed dependencies between builds
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install binutils libproj-dev gdal-bin -y

# Adds our application code to the image
COPY . /code/

# Migrates the database, uploads staticfiles, and runs the production server
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn foodie.wsgi:application
