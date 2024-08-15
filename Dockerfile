FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "social_networking/manage.py", "runserver", "0.0.0.0:8000"]
