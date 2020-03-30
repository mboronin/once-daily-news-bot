FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt && pip install virtualenv
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt
CMD ["/env/bin/python", "main.py"]