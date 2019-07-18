BigData 2019 Course Package, Case 01
====================================


Installation
------------

1. Check [System Requirements](#system-requirements).

1. Install [Prerequisites](#prerequisites).

1. Project setup:
    1. Clone this project from GitHub.
    1. Open Terminal or Windows PowerShell and `cd` to project directory.
    1. Initialize project (run in Terminal or Windows PowerShell): \
            `bigdata19.case01> fab init`
1. Google Cloud Platform setup:
    1. [Register free Google Cloud Platform account](https://cloud.google.com/free).
    1. Create project "bigdata19".
    1. Enable billing for project "bigdata19".
    1. [Create service account](https://support.google.com/cloud/answer/6158849#serviceaccounts)
        for project "bigdata19" with role "Project Owner" and download the JSON key as "secret/gcloud.json".


System Requirements
-------------------

* OS:
    * Mac OS – tested on Mojave 10.14
    * Windows 10 (64-bit) – tested
    * Linux – _not tested_


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
