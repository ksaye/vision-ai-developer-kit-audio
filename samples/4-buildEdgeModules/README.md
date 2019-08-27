# Build the Azure IoT Edge Module

## Overview

This step will build and push the following 2 modules to the Container Registry:
1. audiocapture -- used to record the wav file, via REST post it to the audioinference modules and send a message to Azure IoT Edge
2. audioinference -- a REST endpoint for audioinferencing only

## Requirements

1. Container Registry
2. Docker Desktop installed
3. model files built in 3-buildNetworkWithAzure

## Building audiocapture module

### Configuration File Modification

In samples\4-buildEdgeModules\audiocapture\audiocapture.py modify the following settings:

Setting | Example | Notes
------- | ------- | --------
fileStorageLocation | '/' | where to store the recorded WAV files
sampleStartHour | 0 | what hour to start recording and sending IoT Messages
sampleEndHour | 24 | what hour to stop recording and sending IoT Messages
delayBetweenSampleSeconds | 60 | pause between samples
lengthOfAudioSampleSeconds | 15 | the length of the .WAV file to sample.  this setting must match step 1-audioAquisition

### Building the module

```bash
# log into your Container Registry
docker login --username %UserName% --password %Password% yourcontainerregistry.azurecr.io

# change to the correct directory
cd samples\4-buildEdgeModules\audiocapture

# build the image
docker build . --tag audiocapture

# tage the new image to the repository with the correct tag
docker tag audiocapture yourcontainerregistry.azurecr.io/audiocapture

# push the image to the repository
docker push yourcontainerregistry.azurecr.io/audiocapture
```

## Building audioinference module

### Configuration File Modification

There are no files that request changes.

### Building the module

```bash
# log into your Container Registry
docker login --username %UserName% --password %Password% yourcontainerregistry.azurecr.io

# change to the correct directory
cd samples\4-buildEdgeModules\audioinference

# build the image
docker build . --tag audioinference

# tage the new image to the repository with the correct tag
docker tag audioinference yourcontainerregistry.azurecr.io/audioinference

# push the image to the repository
docker push yourcontainerregistry.azurecr.io/audioinference
```
