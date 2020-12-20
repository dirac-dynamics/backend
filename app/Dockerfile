# pull official base image
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk --no-cache \
        update \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        postgresql-client \
        libpq \
        && apk add --no-cache \
               --upgrade \
               --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
               --virtual .build-deps \
        postgresql-dev \
        zlib-dev jpeg-dev \ 
        alpine-sdk \
        && apk add --no-cache \
               --upgrade \
               --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
        geos \
        proj \
        gdal \
        binutils \
        && ln -s /usr/lib/libproj.so.15 /usr/lib/libproj.so \
        && ln -s /usr/lib/libgdal.so.20 /usr/lib/libgdal.so \
        && ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so

# install dependencies
COPY ./requirements.txt .
RUN  python3 -m pip install --upgrade pip --no-cache-dir \
     && python3 -m pip install -r requirements.txt --no-cache-dir \
     && apk --purge del .build-deps

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]