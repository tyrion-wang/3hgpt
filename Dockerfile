FROM python:3.11
WORKDIR /app/
COPY . /app/.
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN gunicorn -w 10 --threads=2 main:app
#CMD gunicorn 3hgpt.wsgi