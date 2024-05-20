#!/bin/bash

# Aseta Dockerin kontin ja imagen nimet
CONTAINER_NAME="koodiguru_container"
IMAGE_NAME="koodiguru_image"
VOLUME_NAME="my_database_volume"

# Pysäytä ja poista vanha kontti, jos sellainen on olemassa
sudo docker stop $CONTAINER_NAME 
sudo docker rm $CONTAINER_NAME

# Luo uusi Docker image
sudo docker build -t $IMAGE_NAME .

# Luo volyymi, jos sitä ei ole olemassa
sudo docker volume inspect $VOLUME_NAME || sudo docker volume create $VOLUME_NAME

# Käynnistä uusi kontti
sudo docker run --name $CONTAINER_NAME -d -p 8000:8000 -v $(pwd):/app $IMAGE_NAME


# Seuraa kontin lokitusta
sudo docker logs -f $CONTAINER_NAME

