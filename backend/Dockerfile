FROM python:3 as install


# add new user. In Production this increases security. in development this makes developing in the container easier.

ARG USERNAME=django
ARG GROUP=ulti-players
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
WORKDIR /workspace
RUN chown django:django /workspace

USER $USERNAME

RUN mkdir /workspace/backend/ &&\
    mkdir /workspace/backend/backups &&\
    sudo apt update -y && \
    sudo apt install cmake postgresql-client cron -y


RUN pip install --upgrade pip
ADD requirements.txt .
RUN pip install -r /workspace/requirements.txt
ENV PATH="/home/django/.local/bin:${PATH}"

ADD docker-entrypoint.sh /etc/docker-entrypoint.sh
ENTRYPOINT [ "/etc/docker-entrypoint.sh" ]
