# Build the Azure IoT Edge Module

## Overview

This step will build and push the following 2 modules to the Container Registry:
1. audiocapture -- used to record the wav file, via REST post it to the audioinference modules and send a message to Azure IoT Edge
2. audioinference -- a REST endpoint for audioinferencing only

## Current Bug (this section be to removed when resolved)

While it is the intention to run both the audiocapture and the audioinference on the same VAI DevKit, there is a supporting library issue today that causes this to fail.  On ARM32, Librosa has a dependency on numba, which has a dependency on llvmlite.  llvmlite currently does not work on ARM32, as discussed (https://github.com/numba/llvmlite/issues/314) and (https://github.com/piwheels/packages/issues/33).  Once this issue is resolved, the audioinference will build on ARM.  Until then, we have 2 options:

1. run audioinference locally on a non ARM system and change the 'http://audioinference:8080/' in audiocapture.py.  Review Dockerfile.nonARM
2. use an Azure Function, like (https://kevinsaye.wordpress.com/2018/11/06/calling-python-azure-functions-to-process-sound-files/) to process this in the cloud

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

## Building audioinference module (currently not working)

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
