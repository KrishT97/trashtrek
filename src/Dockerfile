FROM python:3.10-slim

WORKDIR /app

COPY application /app/application
COPY requirements.txt /app/requirements.txt
COPY model /app/model

RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/model"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "application/app.py", "--host=0.0.0.0"]
