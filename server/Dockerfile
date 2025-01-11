FROM python:3.13-slim

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
ENV OTEL_METRICS_EXPORTER=none
ENV OTEL_LOGS_EXPORTER=none

CMD ["opentelemetry-instrument", "--traces_exporter", "zipkin_json", "python3.13", "./app.py"]
