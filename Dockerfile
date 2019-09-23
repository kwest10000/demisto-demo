
FROM python:3-alpine

MAINTAINER Kevin East


COPY . /API

WORKDIR /API

RUN pip3 install -r requirements.txt

#EXPOSE 80

CMD ["python3", "app.py"]

