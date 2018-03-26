FROM python:3

RUN mkdir -p /usr/scr/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir  -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uwsgi", "--ini", "/usr/src/app/uwsgi.ini"]