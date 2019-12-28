FROM python:3 as install

# for image_recognition
RUN apt update -y && \
    apt install cmake -y

RUN pip install --upgrade pip
#RUN pip install pipenv
WORKDIR /workspace

#ADD Pipfile /tmp
#RUN cd /tmp && pipenv lock --requirements > requirements.txt  && pipenv --rm
#RUN pip install -r /tmp/requirements.txt
ADD requirements.txt .
RUN pip install -r /workspace/requirements.txt

ADD docker-entrypoint.sh /etc/docker-entrypoint.sh
ENTRYPOINT [ "/etc/docker-entrypoint.sh" ]
