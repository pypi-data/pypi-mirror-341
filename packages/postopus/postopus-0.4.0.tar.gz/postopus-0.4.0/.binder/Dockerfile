FROM registry.gitlab.com/octopus-code/octopus:16.0

USER root
RUN apt-get -y update && apt-get -y install python3 \
            git \
            python3-pip \
            openscad \
            ffmpeg \
            libsm6 \
            libxext6 \
            gnuplot \
            && rm -rf /var/lib/apt/lists/*
# create user with a home directory
ARG NB_USER=postopus_user
ARG NB_UID=1000
ENV USER="$NB_USER"
ENV NB_UID="$NB_UID"
ENV HOME="/home/$NB_USER"
ENV OMP_NUM_THREADS=10

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY . ${HOME}/postopus
USER root
RUN chown -R ${NB_UID} ${HOME}

USER ${NB_USER}
# install the notebook package
RUN pip install --break-system-packages --no-cache --upgrade pip && \
    pip install --break-system-packages --no-cache notebook jupyterlab && \
    pip install --break-system-packages --no-cache -e ${HOME}/postopus[recommended]
# the command `jupyter` is provided in `~/.local/bin` and required by the binder launcher.
ENV PATH="$HOME/.local/bin:$PATH"
WORKDIR ${HOME}/postopus
