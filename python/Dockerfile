FROM python:latest

ENV PYTHONUNBUFFERED=1

# Default to local timezone
ENV TZ=America/Detroit
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt -y update && apt install -y nano wget curl net-tools

# Copy cron schedules
COPY ./cron/rdt /etc/cron.d/

# Set up project directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install package requirements
COPY ./requirements.txt /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN cron -f