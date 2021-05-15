FROM python:3.6.1-alpine
WORKDIR /usr/src/app
RUN pip install flask
COPY ./app ./app
CMD ["python", "./app/sortinghat.py"]
