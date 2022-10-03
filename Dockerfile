FROM python:3.9

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt \
    pip install psycopg2-binary

COPY . /nurbank_drf
WORKDIR /nurbank_drf/api
