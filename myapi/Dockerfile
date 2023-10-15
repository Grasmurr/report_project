FROM python:3.10.5

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install gunicorn
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=myapi.settings
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "myapi.wsgi:application", "--bind", "0.0.0.0:8000"]
