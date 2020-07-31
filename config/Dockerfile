FROM python:3.7-slim

RUN apt-get update && apt-get install -y netcat

# Set working directory
WORKDIR /opt/qualichain_backend

# Install Project requirements
COPY application/requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD bash config/run.sh