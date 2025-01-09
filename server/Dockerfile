FROM python:3.9

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
RUN opentelemetry-bootstrap --action=install

#Set the working directory
WORKDIR /usr/src/app

#copy all the files
COPY . .

#Run the command
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

CMD ["opentelemetry-instrument", "--metrics_exporter", "console", "--traces_exporter", "console", "--logs_exporter", "console", "python3.9", "./app.py"]
