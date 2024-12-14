FROM python:3.12-alpine3.21

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
