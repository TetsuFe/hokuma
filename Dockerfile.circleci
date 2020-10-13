FROM python:3.6.2
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/hokudai_furima/static
WORKDIR /usr/src/app
ADD Pipfile /usr/src/app/
ADD Pipfile.lock /usr/src/app/
RUN pip install pipenv
RUN pipenv install --system --deploy --skip-lock
ADD . /usr/src/app/