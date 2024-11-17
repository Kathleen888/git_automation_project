FROM python:3.10-slim

# Installeer Git
RUN apt-get update && apt-get install -y git

# Maak de map /dnt2 aan
RUN mkdir -p /dnt/2024_DS1_Mechelen

# Maak de map /workdir aan
RUN mkdir -p /workdir

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY pull_and_copy.py pull_and_copy.py

CMD ["python","pull_and_copy.py"]