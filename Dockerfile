FROM python:3.11

WORKDIR /server

COPY requirements.txt server/conf/requirements.txt

RUN pip install --no-cache-dir --upgrade -r server/conf/requirements.txt

COPY requests /server

CMD bash -c "while true; do sleep 1; done"