FROM python:3.6-stretch

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt

COPY uwsgi_docker.ini /uwsgi_docker.ini

COPY bankthing /app/bankthing
COPY tests /app/tests
WORKDIR /app

EXPOSE 8080
ENTRYPOINT ["uwsgi", "--ini", "/uwsgi_docker.ini"]
