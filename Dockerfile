#RUN pip install --upgrade pip

RUN echo 'we are running some # of cool things'
CMD gunicorn -w 10 --threads=2 main:app