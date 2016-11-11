FROM python:3.4

# Copy all project files and chdir
COPY . /opt/lagmonitor
WORKDIR /opt/lagmonitor

# Install requirements
RUN pip install -r requirements.txt

RUN pip install -e .

EXPOSE 8080
CMD [ "python", "-u", "/opt/lagmonitor/lagmonitor/main.py", "--config-file", "/opt/lagmonitor/config.yaml"]
