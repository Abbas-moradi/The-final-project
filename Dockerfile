FROM python:3.11

LABEL maintainer="en.moradi.66@gmail.com"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=OnloneShop.settings

RUN python manage.py makemigrations

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "OnloneShop.wsgi:application"]
