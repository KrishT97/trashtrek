FROM python:3.10-slim

WORKDIR /app

COPY application /app/application
COPY requirements.txt /app/requirements.txt
COPY model /app/model

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/model"

EXPOSE 5000

CMD ["python", "application/app.py", "--host=0.0.0.0"]
