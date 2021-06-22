FROM python:3.9-slim-buster

ADD geo_agent.py .
ADD geo_elastic.py .
ADD geo_minio.py .
ADD geo_zabbix.py .

RUN pip install --no-cache-dir pyzabbix
RUN pip install --no-cache-dir elasticsearch[async]
RUN pip install --no-cache-dir loguru
RUN pip install --no-cache-dir minio

CMD [ "python", "./geo_agent.py"]
