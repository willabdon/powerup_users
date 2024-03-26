FROM python:3.12

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "users.wsgi", "-b", "0.0.0.0:8000"]
