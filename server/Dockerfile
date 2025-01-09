FROM python:3.9

#Set the working directory
WORKDIR /usr/src/app

#copy all the files
COPY . .

#Install the dependencies
RUN pip install -r requirements.txt
RUN opentelemetry-bootstrap --action=install

# # #Run the command
CMD ["python ./app.py"]