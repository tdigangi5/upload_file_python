FROM python:2.7.14-jessie
MAINTAINER vision_io "vision@vision.io"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /src
WORKDIR /src
RUN pip install -r src/requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS='/src/digangi-first-project-52abe234754d.json'
ENTRYPOINT ["python"]
CMD ["src/app.py"]
