FROM hub.hamdocker.ir/library/python:3.11
WORKDIR /website/
COPY config/gunicorn_conf.py /app/config/gunicorn_conf.py
ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt
ADD ./ ./
RUN ls -l /website/static/
ENTRYPOINT ["/bin/sh", "-c" , "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 website.wsgi"]