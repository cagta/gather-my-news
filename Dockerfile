FROM python:3
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src ./code

LABEL maintainer="https://www.linkedin.com/in/cagatay-tanyildiz/"

CMD ["python","./code/gather.py"]
