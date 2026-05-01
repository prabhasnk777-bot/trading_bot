FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 5000
ENV PORT=5000

# Use gunicorn to bind to the port supplied by the hosting provider
CMD gunicorn --bind 0.0.0.0:$PORT web:app
