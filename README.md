# NC DOT Roadway Safety Annotation Tool

The overall goal of the tool is to build an ML/AI system for associating annotations with roadway images.  For many features of interest, we will initially focus on a binary presence/absence of a feature such as a guardrail, a sign, or a tree. We will develop an off-line neural net to detect these features, but the network needs annotations for training.  The network will then predict annotations on un-annotated frames with prediction certainty score, and users will be able to view, update, and accept or reject the predicted annotations. 

The annotation tool is implemented using the [Docker](https://www.docker.com/) platform and [Django](https://www.djangoproject.com/) web framework on the server backend. It currently uses [iRODS](https://irods.org/) for data management although iRODS is designed as an optional component so that the tool can also run on other data management platform such as in the cloud environment.

## Install
This section is aimed for developers interested in working on the code. It provides guidance for setting up docker-based Django server local development environment for the tool.

### Prerequisite
[Docker](https://www.docker.com/ "Docker") and [Docker Compose](https://docs.docker.com/compose/ "Docker Compose") need to be installed. On Windows 10 and above, native Docker may be installed and used. Otherwise, a Linux VM is needed.

### Steps to run the annotation tool web server in your local development environment
- Clone source code from this repo.
- Get ```local_settings.py``` that contains iRODS access credentials from txscience project directory. This local_settings.py holds sensitive information, so should not be exposed to the outside world.
- Change ```UID``` (default is ```1000```) and ```GID``` (default is ```1000```) in ```server/docker-compose.yml``` as needed to correspond to the uid and gid of the user on the host who is running docker containers for the tool. The default values should cover most if not all cases in a local development environment.
- From the ```server``` directory of the source tree, run ```./up.sh``` to build all containers.
- At this point you should be able to open up your browser to get to the tool home page: http://localhost:8000, or http://192.168.56.101:8000/ from the host if host-only adaptor is set up in VirtualBox for the Linux VM running on a windows box.
- From the ```server``` directory of the source tree, run ```./down.sh``` to bring down and clean up all containers. Alternatively, you can run ```docker-compose stop``` followed by ```docker-compose up``` if you want to keep the states of all containers for continuous development.


### Useful docker-compose commands to manage docker containers 
- ```docker-compose up``` --- bring up all containers
- ```docker-compose stop``` --- stop all containers
- ```docker-compose ps``` --- check status of all containers
- ```docker rm -fv $(docker ps -a -q)``` --- remove all containers
- ```docker rmi -f <image_id>``` where ```<image_id>``` is the image id output from ```docker images``` command which you want to remove. 

