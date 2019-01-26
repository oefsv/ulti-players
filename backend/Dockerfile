FROM ubuntu

RUN apt-get update && \
  apt-get install -y apt-utils vim curl apache2 apache2-utils && \
  apt-get -y install python3 libapache2-mod-wsgi-py3 && \
  ln /usr/bin/python3 /usr/bin/python && \
  apt-get -y install python3-pip && \
  ln /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip
RUN pip install django ptvsd

COPY requirements.txt /
COPY . /var/www/html/backend/
RUN pip install -r /requirements.txt
ADD ulti-players-backend.conf /etc/apache2/sites-available/000-default.conf
EXPOSE 80 3500
CMD ["apache2ctl", "-D", "FOREGROUND"]
