FROM python:3.10

RUN pip install pipenv

COPY . /app
WORKDIR /app
RUN pipenv install --deploy

CMD pipenv run python ./change_container_ip.py