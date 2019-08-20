FROM debian:10-slim

# OS

RUN set -ex && \
    apt-get update && \
    apt-get install -y --no-install-recommends apt-utils curl && \
    rm -rf /var/lib/apt/lists/*

# Python 3, Pip, Pandas, Sklearn

RUN set -ex && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pandas \
        python3-pip \
        python3-sklearn \
        && \
    python3 -m pip install --no-cache --upgrade pip setuptools wheel && \
    rm -rf /var/lib/apt/lists/*

# Java

RUN set -ex && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-transport-https ca-certificates dirmngr gnupg software-properties-common && \
    curl -s https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - && \
    add-apt-repository -y https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ && \
    apt-get update && \
    mkdir -p /usr/share/man/man1 && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends adoptopenjdk-8-hotspot && \
    rm -rf /var/lib/apt/lists/*

# Spark

ARG SPARK_VERSION=2.4.3
ARG HADOOP_VERSION=2.7

ARG SPARK_HOME=/opt/spark
ENV SPARK_HOME=${SPARK_HOME}

RUN set -ex && \
    curl -s -o /tmp/spark.tgz http://apache.mirror.anlx.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mkdir ${SPARK_HOME} && \
    tar -xzf /tmp/spark.tgz -C ${SPARK_HOME} --strip-components 1 && \
    rm /tmp/spark.tgz

# PySpark

RUN set -ex && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends pandoc  && \
    cd ${SPARK_HOME}/python && \
    python3 setup.py sdist && \
    python3 -m pip install dist/*.tar.gz && \
    rm dist/*.tar.gz && \
    rm -rf /var/lib/apt/lists/*
# spark wants "python" command on path
RUN set -ex && \
    ln -s /usr/bin/python3 /usr/bin/python

# Other Python packages

RUN set -ex && \
    python3 -m pip install --no-cache \
        aiofiles \
        aiohttp \
        invoke \
        lxml \
        pyspark \
        pyspark-stubs \
        pyyaml \
        tqdm

# Run

ARG SPARK_PORT=7077
ARG SPARK_WEBUI_PORT=8080
EXPOSE 7077 8080
ENV SPARK_PORT=${SPARK_PORT}
ENV SPARK_WEBUI_PORT=${SPARK_WEBUI_PORT}

ENV SPARK_SERVICE=master
ENV SPARK_MASTER_HOST=master

CMD if [ ${SPARK_SERVICE} = master ]; \
    then \
        spark-class org.apache.spark.deploy.master.Master \
            --host `hostname` --port ${SPARK_PORT} --webui-port ${SPARK_WEBUI_PORT}; \
    else if [ ${SPARK_SERVICE} = worker ];\
        spark-class org.apache.spark.deploy.worker.Worker \
            --host `hostname` --webui-port ${SPARK_WEBUI_PORT} spark://${SPARK_MASTER_HOST}:${SPARK_PORT}; \
    else \
        bash; \
    fi
