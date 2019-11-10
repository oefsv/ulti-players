FROM python:3 as install

RUN pip install --upgrade pip
RUN pip install pipenv
WORKDIR /workspace

ADD Pipfile /tmp
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt