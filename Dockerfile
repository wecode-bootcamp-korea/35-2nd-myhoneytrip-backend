FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["nohup", "gunicorn", "--bind", "0.0.0.0:8001", "myhoneytrip.wsgi", "&"]