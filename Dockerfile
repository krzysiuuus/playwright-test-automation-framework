FROM python:3.14-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium firefox webkit

COPY . .

CMD ["pytest"]