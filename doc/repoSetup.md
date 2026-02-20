# Setting up the LazerShark repo
The purpose of this document is to record the process taken to set up the `LazerShark` repository.


## Setting up the ros project
1. Install docker
    ```
    sudo apt install docker.io git python3-pip
    pip3 install vcstool
    echo export PATH=$HOME/.local/bin:$PATH >> ~/.bashrc
    source ~/.bashrc
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```
1. Create  `.devcontainer` folder
    ```
    mkdir .devcontainer
    ```
1. Add `devcontainer.json` to name the container and include the image
    ```
    cd .devcontainer
    touch devcontainer.json
    ```
1. Create `Dockerfile`
    ```
    touch Dockerfile
    ```
    Add content to dockerfile
1. Create `setup` directory at the root
    ```
    cd .. 
    mkdir setup
    ```

I did a lot more here but I am unsure if what I did makes sense. I will add it if it works