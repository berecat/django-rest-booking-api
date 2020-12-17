FROM python:3.8.3-alpine

WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./docker_files/entrypoint.sh ./docker_files/

COPY . .

ENTRYPOINT ["/usr/src/app/docker_files/entrypoint.sh"]