###########
# BUILDER #
###########

FROM python:alpine3.16 as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev curl libffi-dev

# install poetry
ENV POETRY_HOME /etc/poetry
RUN mkdir ${POETRY_HOME}
RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install --upgrade pip
RUN ${POETRY_HOME}/bin/pip install poetry==1.2.0

COPY . .
RUN ${POETRY_HOME}/bin/poetry build --no-cache --format=wheel


#########
# FINAL #
#########

FROM python:alpine3.16

# create user
RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq gcc musl-dev build-base
COPY --from=builder /usr/src/app/dist /wheels
RUN pip install --no-cache /wheels/*.whl

RUN chown -R app:app $APP_HOME
USER app

CMD python -m app.__main__