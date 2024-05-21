FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y ghostscript && \
    pip install Flask

COPY ./app /app
WORKDIR /app

CMD ["python", "gs_service.py"]
