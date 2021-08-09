FROM renci/ncdot_docker_base:1.5

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

# create the app user
RUN groupadd --system app && useradd --system -g app --shell /bin/bash --home /home/app app

# chown all the files to the app user
RUN chown -R app:app $HOME
RUN usermod -u $UID app
RUN groupmod -g $GID app

# change to the app user
USER app
WORKDIR $APP_HOME
