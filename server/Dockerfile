FROM renci/ncdot_docker_base:1.1

ARG UID
ARG GID
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="${PYTHONPATH}:/usr/share/"

# set work directory
ENV HOME=/home/app
ENV APP_HOME=/home/app/server
# create directory for the app user and the server directory
RUN mkdir -p $APP_HOME/static

# create directory for the mounted image directory which is needed when USE_IRODS flag is FALSE
RUN mkdir -p $APP_HOME/data

# create the app user
RUN groupadd --system app && useradd --system -g app --shell /bin/bash --home /home/app app

# chown all the files to the app user
RUN chown -R app:app $HOME
RUN usermod -u $UID app
RUN groupmod -g $GID app

# change to the app user
USER app
WORKDIR $APP_HOME
