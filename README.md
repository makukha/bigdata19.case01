BigData 2019 Course, Case #1
============================

This repository contains Python code of Case Study #1 for BigData19 course.

1. [Case Study Scope](#case-study-scope)
    * [Topics](#topics)
    * [Tools](#tools)
1. [System Requirements](#system-requirements)
1. [Installation](#installation)
1. [Prerequisites](#prerequisites)
1. [Usage](#usage)


Case Study Scope
----------------

### Topics

1. Synchronous and asynchronous web scraping.
1. Managing Google Cloud Platform resources.
1. Reading and writing data to/from multiple sources and formats.
1. Web scraping on a Spark cluster.
1. Machine Learning on a Spark cluster.

### Tools

* Python:
    * aiofiles, aiohttp, asyncio
    * csv
    * [Fabric](http://www.fabfile.org), tqdm
    * pyspark, pyarrow
* Google Cloud Platform:
    * Google BigQuery
    * Google Cloud Storage
    * Google Dataproc
* Docker
* Apache Spark + MLlib
* Apache Arrow
* Apache Cassandra
* Elasticsearch + Kibana
* Airflow
* Git, GitHub
* PyCharm, Atom


System Requirements
-------------------

Tested on:

* Mac OS Mojave 10.14  with Docker Desktop
* Windows 10 Pro (64-bit) with Docker Desktop
* Windows 10 Home (64-bit) with Docker Toolbox

Linux – _not tested_.


Installation
------------

1. Check [System Requirements](#system-requirements).

1. Install [Prerequisites](#prerequisites).

1. Project setup:
    1. Fork this project to your account on GitHub.
    1. Clone your fork.
    1. Open Terminal or Windows PowerShell and `cd` to project directory.
    1. Initialize project (run `fab init` in Terminal or Windows PowerShell)

1. Google Cloud Platform setup:
    1. [Register free Google Cloud Platform account](https://cloud.google.com/free).
    1. Create project "bigdata19".
    1. Enable billing for project "bigdata19".
    1. [Create service account](#create-gcp-service-account)
        for project "bigdata19" with role "Project Owner" and save the JSON key to file "secret/gcloud.json".


Prerequisites
-------------

### Anaconda Python 3.7 (64-bit)

Install latest [Anaconda with Python 3.7](https://www.anaconda.com/distribution/) (64-bit version) with  options:

* [x] Just Me (recommended)
* [x] Add Anaconda to the system PATH envitronment variable
* [x] Register Anaconda as the system Python 3.7

#### Verify installation

Open **new window** of Terminal or Windows PowerShell.

* Anaconda

        > conda --version
        conda 4.6.11
    
* Python

        > python --version
        Python 3.7.3


### Fabric

In this project we use [Fabric](http://www.fabfile.org) for automation:

    > conda install -y fabric

#### Verify installation

    > fab --version
    Fabric 2.4.0
    Paramiko 2.4.2
    Invoke 1.2.0


### Docker

Install free [Docker Desktop Community Edition](https://hub.docker.com/search/?type=edition&offering=community).

#### Verify installation

* Docker is installed:

        > docker --version
        Docker version 18.09.2, build 6247962
    
* Docker can create containers:

        > docker run --rm busybox echo "Hello!"
        Hello!
    
If something goes wrong and you are unable to run commands above,
please carefully follow the installation instructions for your system
(you may even need to change BIOS settings):

* [Install Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
* [Install Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)


## Google Cloud Platform

### Create GCP Service Account

See this screencast: [Create Service Account for GCP Project](https://www.youtube.com/watch?v=6tWWc4dhrbM).

THe JSON file downloaded in this video must be renamed as "gcloud.json" and put into folder "/secret".


Usage
-----

### Manage and Run the Project

* `fab init` — Initialize or update the project.
* `fab run assignment02.py` — Run Assignment 02.

### Manage Google Cloud Platform Resources

* `fab cloudsdk "{gcloud|gsutil|...} args"` — Run arbitrary CloudSDK commands.
* `fab cluster list` — List Dataproc clusters.
* `fab cluster create` — Create Dataproc cluster.
* `fab cluster delete` — Delete Dataproc cluster.
