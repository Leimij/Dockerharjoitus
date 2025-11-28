FROM python:3.12-slim

WORKDIR /app

# Asenna flask suoraan
RUN pip install flask

COPY . .

CMD ["python", "server.py"]
