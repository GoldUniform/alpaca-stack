FROM ubuntu:latest
RUN apt-get update --fix-missing
RUN apt-get install -y python3-pip python3 build-essential
COPY ./position_exporter/ /app
COPY ./config.yml /app/config.yml
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["position_exporter.py"]