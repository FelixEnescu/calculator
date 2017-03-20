FROM python:2.7
MAINTAINER Felix Enescu <felix@enescu.name>

ADD ./app /app
WORKDIR /app/

RUN pip install -r requirements.txt

CMD python app.py
