# AI Tool with Active Learning for Detection of Rural Roadside Safety Features

In collaboration with North Carolina Department of Transportation (NCDOT), UNC highway safety research center (HSRC), and
DOT Volpe national transportation systems center, we at UNC Renaissance Computing Institute (RENCI) developed roadside
feature models using convolutional neural networks (CNNs) in an iterative active learning (AL) pipeline integrated into an AI
tool to detect safety features such as guardrails and utility poles in dispersed NC rural roads. We utilized transfer learning to extract a common feature backbone that was then used in an iterative AL process supported by a web-based annotation tool. The annotation tool not only allows us to collect annotations through an iterative AL process for multiple safety features, it also enables visual analysis and assessment of model prediction performance in the geospatial context. AL techniques were used to direct human annotators to label images that would most effectively improve the model aimed at minimizing the number of required training labels while maximizing the model’s performance. The iterative AL process with a common feature extraction backbone allowed fast model inference on millions of images in the AL sampling space enabling a rapid transition between AL rounds. Model weights were then fine tuned in the last round of AL to obtain the best accuracy for the final model. Our AI tool can be used to detect other roadside safety features and be extended to also locate them for assessing roadside hazard rating.

The web-based annotation tool is implemented using the [Docker](https://www.docker.com/) platform, [Django](https://www.djangoproject.com/) web framework on the server backend, and [React](https://reactjs.org/) JavaScript library on the client frontend. [iRODS](https://irods.org/) is also used as an optional middleware component to manage and transfer images for local development on any personal computer. If the tool is deployed on a server with the data volume mounted directly, iRODS can be easily turned off by setting `USE_IRODS` environment variable to `False`. 

## Install
This section is aimed for developers interested in working on the code. It provides guidance for setting up docker-based Django server local development environment for the tool.

### Prerequisite
[Docker](https://www.docker.com/ "Docker") and [Docker Compose](https://docs.docker.com/compose/ "Docker Compose") need to be installed. On Windows 10 and above, native Docker may be installed and used. Otherwise, a Linux VM is needed.

### Steps to run the annotation tool web server in your local development environment
- Clone source code from this repo.
- Get ```local_settings.py``` that contains iRODS access credentials from txscience project directory and copy it to ```server/road_safety``` directory. This local_settings.py holds sensitive information, so should not be exposed to the outside world.
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

