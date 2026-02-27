FROM docker.io/eprosima/vulcanexus:humble-desktop

# Setup packages needed for `make devbox-install`
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install git ansible python3-pip vim sudo 

# Install the latest devbox playbook from git
COPY . /dev-setup
RUN cd /dev-setup \
    && ansible-playbook \
		--connection=local \
		--inventory 127.0.0.1, \
		--limit 127.0.0.1 devbox.yaml \
    && rm -rf /dev-setup \
    && apt clean 

ARG USERNAME=student
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV DEBIAN_FRONTEND=noninteractive

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -s /usr/bin/bash -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

# FIXME: NOT SURE IF WE NEED THE FOLLOWING
# Copy source for future tooling.
# COPY --chown=$USERNAME:$USERNAME src/ /tmp/dep-repos/src 
# WORKDIR /tmp/dep-repos 

# WORKDIR /home/${USERNAME}
# RUN sudo rm -rf /tmp/dep-repos 
# COPY .devcontainer/default.bashrc /home/${USERNAME}/.bashrc