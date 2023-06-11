FROM python:3.10.0-slim
WORKDIR /
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN echo 'we are running some # of cool things'
RUN pip install -r requirements.txt
CMD gunicorn -w 10 --threads=2 main:app