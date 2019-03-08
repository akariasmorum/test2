FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD gunicorn -w 2 -b 0.0.0.0:8001 run:app

