FROM python:3.9

WORKDIR /usr/src/telegram_bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_bot/ .
ENV PYTHONPATH=/usr/src/telegram_bot

CMD ["python", "./main.py"]
