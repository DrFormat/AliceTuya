### --- Build pip packages --- ###
FROM python:3.11-alpine3.16 as build
LABEL maintainer="Andrey Borodachev <formacevt@bk.ru>"

ENV WORKDIR=/opt/app \
    WHEELDIR=/opt/pip_packages

WORKDIR $WORKDIR

RUN apk --no-cache add --virtual build-dependencies \
    gcc \
    g++ \
    musl-dev \
    linux-headers \
    make \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    postgresql-dev \
    openssl-dev \
    cargo \
    git

COPY requirements.txt $WORKDIR
RUN pip wheel --wheel-dir=${WHEELDIR} -r requirements.txt \
    && rm -rf .cache/pip

### --- Final small image --- ###
FROM python:3.11-alpine3.16

ENV WORKDIR=/opt/app \
    WHEELDIR=/opt/pip_packages \
    TZ=Europe/Samara

WORKDIR $WORKDIR

RUN apk add --no-cache libpq \
    libxslt \
    gcc \
    musl-dev \
    linux-headers \
    libc-dev \
    libressl-dev \
    zlib-dev \
    openssl-dev \
    xmlsec \
    git \
    tzdata

RUN cp /usr/share/zoneinfo/Europe/Samara  /etc/localtime

COPY --from=build ${WHEELDIR} ${WHEELDIR}
COPY requirements.txt $WORKDIR

RUN pip install -r requirements.txt --find-links=${WHEELDIR} \
    && rm -rf .cache/pip

COPY . $WORKDIR
#COPY .deploy/wait-for-postgres.sh $WORKDIR
#COPY .deploy/run_tests.sh $WORKDIR

EXPOSE 8000

CMD ["gunicorn", "app.asgi:app", "-b", "0.0.0.0:8000", "-w", "1", "-k", "app.uvicorn_worker.UvicornWorker"]
