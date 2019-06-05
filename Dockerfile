FROM python:3.7.2
WORKDIR /app
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
COPY ./application /app/application
ENV $$TORCH_MODEL_ZOO=/data/models

