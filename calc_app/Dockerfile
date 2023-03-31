FROM python:2.7

ADD ./app /app
WORKDIR /app/

RUN apt update \
    && pip install -r requirements.txt \
    && pip install nose \
    && pip install pytest \
    && pip install flake8

CMD python app.py
