# Collecting Sample Audio Files

To build an appropriate model, numerous sample files are needed for each lable of an event.  Our example solution measures how full a water fountain is by percentage in increments of 10 (10%, 20%, 30% etc).

This docker file builds a container that samples and uploads the wav files to an Azure Blob Storage account to be labeled later.

For the highest accuracy, this container should be run on the same device that will be used for later inferencing.

## Configuring the container

Modify the audioAquisition.py file for the following settings.

Setting | Example | Notes
------- | ------- | --------
azureStorgeAccountName | 'myaudiostorgeaccount' | the name of your Azure Blob Storge Account
azureStorageKeyName | 'dMCtRc7OGw==' | the primary or secondary key of your Azure Blob Storage Account
azureStorageContainer | 'newfountain' | the Blob container in the storage account.  it will be created if it does not exist
fileStorageLocation | '/' | where to save the .WAV files in the container
sampleStartHour | 17 | what hour to start sampling in the day.  to sample all the time, set the value to 0
sampleEndHour | 22 | what hour to stop sampling in the day.  to sample all the time, set the value to 24
delayBetweenSampleSeconds | 60 | pause between samples
lengthOfAudioSampleSeconds | 15 | the length of the .WAV file to sample.  this setting must match step 4-buildEdgeModules

Modify the DockerFile if you prefer a timezone other than Chicago.

## (option 1) Building and running the container with a Container Registry

The container to aquire audio files can be built remotely and pulled from a Container Registry or build local.  This instruction uses a Container Registry.

### Requriements

On your build machine, you need the following:
1. Docker Desktop configured for Linux Containers
2. Access to a Container Registry (Azure Container Registry or DockerHub)

To configure your docker to use the Container Registry, run the command:
```bash
docker login --username %UserName% --password %Password% yourcontainerregistry.azurecr.io
```

### Build and Push to the Container Registry

To build the image run:
```bash
# change to the correct directory
cd samples\1-audioAquisition

# build the image
docker build . --tag audio

# tage the new image to the repository with the correct tag
docker tag audio yourcontainerregistry.azurecr.io/audio

# push the image to the repository
docker push yourcontainerregistry.azurecr.io/audio
```

### Pull and Run from the Container Registry

Log into the VAI DevKit either via SSH or the USB cable and run the following commands:

```bash
# first we have to remount the root file system so we can write docker login files
# for this to work you need to know the root password.  You can reset it via the USB cable
sudo mount -o remount,rw /

# login to your Container Registry
docker login --username %UserName% --password %Password% yourcontainerregistry.azurecr.io

# create the container with the --privileged command
docker create --privileged --name audio yourcontainerregistry.azurecr.io/audio 

# run the container
docker run audio

# remount the root filesystem back to read only
sudo mount -o remount,ro /
```

## (option 2) Building and running the container without a Container Registry

The container to aquire audio files can be built remotely and pulled from a Container Registry or build local.  This instruction builds locally without a Container Registry.

Log into the VAI DevKit either via SSH or the USB cable and run the following commands:
```bash

cd /tmp
mkdir audio
cd audio

# using copy and past past the contents from DockerFile into this file
vim DockerFile

# using copy and past past the contents from audioAquisition.py into this file
vim audioAquisition.py

# build the image
docker build . --tag audio

# create the container with the --privileged command
docker create --privileged --name audio audio 

# run the container
docker run audio

```

## Verifying data is being collected

Log into the [Azure Portal](http://portal.azure.com) to verify your .WAV files are being uploaded into the named container during the allowed hours.

Alternatively, on the VAI DevKit, you can run the following command:
```bash
docker logs -f audio
```
