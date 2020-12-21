# pull official base image
FROM gboeing/osmnx

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

USER root
RUN apt-get update && apt-get install -y netcat

RUN apt-get install -y binutils libproj-dev libgdal-dev g++ --no-install-recommends && \
    apt-get clean -y

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

# install dependencies
COPY ./requirements.txt .
RUN  python3 -m pip install --upgrade pip --no-cache-dir \
     && python3 -m pip install -r requirements.txt --no-cache-dir

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]