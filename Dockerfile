FROM ubuntu:latest
WORKDIR /website/


RUN apt update && apt install supervisor nginx python3-pip libpq-dev python3-dev -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV ALLOWED_HOSTS=localhost

# RUN python manage.py migrate
RUN python3 manage.py collectstatic

COPY etc/apps-supervisor.conf /etc/supervisor/conf.d/apps-supervisor.conf
COPY etc/nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/bin/supervisord"]


