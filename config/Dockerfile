FROM python:3.7-slim

# Set working directory
WORKDIR /opt/flask-docker-backbone

# Install Project requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD bash config/run.sh