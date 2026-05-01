FROM cgr.dev/chainguard/python:latest-dev

WORKDIR /app

ENV PYTHONOPTIMIZE=2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["app.py"]