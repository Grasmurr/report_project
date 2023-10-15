FROM python:3.9

WORKDIR /usr/src/telegram_bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/usr/src

CMD ["python", "./main.py"]
