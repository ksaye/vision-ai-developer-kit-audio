# Vision AI Developer Kit for Audio Processing

## Overview

This sample solution breaks down the audio processing into 5 phases:
1 Audio file aquisition from the Vision AI Developer Kit (VAI DevKit) microphone to Azure Storage
2 Label a copy of the audio files in Azure Storage
3 Building a Neural Network for processing audio files using Azure Machine Learning Workspace
4 Building the Azure IoT Edge modules for inferencing the audio sounds
5 Deploying the modules to Azure IoT Edge

## Assumptions

This sample is focused on audio processing.  It is assumed that you already have an understanding and experience with:
* [Azure IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart)
* [Vision AI DevKit](https://azure.github.io/Vision-AI-DevKit-Pages/docs/Get_Started/)
* [Docker Desktop](http://www.docker.com)
* [Python on Visual Studio Code](https://code.visualstudio.com/docs/languages/python)
* [Azure Machine Learning Service](https://docs.microsoft.com/en-us/azure/machine-learning/service/)
* [Basic understanding of Machine Learning](https://en.wikipedia.org/wiki/Machine_learning)
* [Basic understanding of Supervised Learning](https://en.wikipedia.org/wiki/Supervised_learning)

## Sample Solution

To build any Machine Learning Model, you need plenty of sample data.  Audio is no different.  For our example we will predict the water level of an 8 foot fountain, just by the sound.  Water is a common sound that most people can understand.  Think about a leaky faucet where drops of water go into an empty sink.  Then think about the same leaky faucet, but this time the sink is 1/2 full and then a full sink.  You can imagine the difference in sounds.  One is higher pitch, one is lower pitch with a more hollow sound.  This is the premise we will work from for our sample, but honestly it can be the comparison of any sound.  Consider:
* a squeeking bearing on a motor.
* the RPMs (revolutions per minute) of a vehicle.  
* the suction sound of a vacuum pump

Compare these 2 sounds from our fountain:
* [Our fountain full](https://github.com/ksaye/IoTDemonstrations/blob/master/audioWave/201805211827-fountain.wav?raw=true)
* [Our fountain 1/2 full](https://github.com/ksaye/IoTDemonstrations/blob/master/audioWave/201806151709-fountain%20(1550).wav?raw=true)

With your eyes closed, you can hear the difference.  Perhaps you can't explain the difference in words, but that is where programs and computers come in.

## Audio File Aquisition

To build our model, we need LOTS of samples and we need to label them appropriately.  For the best results, we need to sample the images on the same hardware (microphone) that we will be inferencing with.  For our sample solution, audio file aquisition was simple, just record enough sounds from the VAI DevKit with the fountain full, and then record with the fountain 1/2 full, then empty.  To make this more elegant, I actually recorded sound for a month straight.  Imaging on the first day of the month, the fountain is full and for the next 30 days we sample 100s of sounds per day up to the end of the month or when ever the fountain is verified to be empty.  Using this approach I captured 3,600 15-second wave files for a total of over 9 GB in files -- and I consider this a bare minimimum.  Why so many sound samples?  This fountain is inside a house.  Imagine a dog barking, the doorbell ringing, the radio playing or a person laughing.  Many distractions, so we let the sheer number of audio files overcome these anomalities.  For our sample, WAV files are the format that include the needed fidelity which allow us to extract the needed features.  With so many samples and assuming even evaporation of the water, we can now determine how full the fountain is.  For this sample, we determine by percent from 100%, 90%, 80% and so on. 

You can find the DockerFile for audio aquisition approach in samples\1-audioAquisition.  Simply stated, it runs a loop during defined hours to collect 15 second wav files and uploads these to an Azure Blob storage for later processing.

## Labeling the audio files

So far we just have a storage account with audio samples that do not have any label.  Because we aquired the sound files in such a seqential fashion, we can easily label the first 10% as '100% full', the next 10% as '90% full' and so on until we get to the last 10%.  Our labeling system is [100%, 90%, 80%, 70%, 60%, 50%, 40%, 30%, 20%, 10%], which means we have 10 'classes'.  To make this easy, we will rename each file from ############.WAV to ############-NNN.WAV, where -NNN is the label, such as -100 or -30.  As a best practice, I always leave the source data intact, so technically instead of reanaming the files, I copy them from one container to anonther, renaming the file as I copy it.

You can find the labeling script in samples\2-lableFiles

## Building the Neural Network

Building our Neural Network will be Diffusion-Convolutional Neural Network, based on the work of [Xianshun Chen](https://github.com/chen0040) shared [here](https://github.com/chen0040/keras-audio).  Here we will use Keras-Audio, and a few supporting Python libraries to build the model.

With the audio files labled and using Azure Machine Learning Service Workspace, we can built the model.  For larger data sets, we can use a GPU for model building which makes the process go much faster.  For this sample, and leveraging the power of Azure, I performed distributed training using 4 nodes using different sized host.

Processing ~3.6K images using 50 epcochs with a batch size of 8 and with the melspectrograms already calculated takes the following times:

Compute SKU | Nodes | val_acc | Time to Process | [Azure Calculator Cost](https://azure.microsoft.com/en-us/pricing/calculator/)
----------- | ----- | -------- | --------------- | ------------
[STANDARD_D2](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-previous-gen#older-generations-of-virtual-machine-sizes) | 1 | x | time | $.11 per hour * = 
[STANDARD_D2](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-previous-gen#older-generations-of-virtual-machine-sizes) | 4 | 0.9381 | 20h 53m 16.53s | 4 x $.11 per hour x 20.88 = **$9.20**
[STANDARD_D14](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-previous-gen#older-generations-of-virtual-machine-sizes) | 1 | 0.9446 | 5h 13m 31.44s | $1.33 per hour x 5.225 = **$6.95**
[STANDARD_NC6](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/sizes-gpu#nc-series) | 1 | 0.9446 | 21m 20.96s | $2.46 per hour x .35 = **$0.87**

You can find the Build Network script in samples\3-buildNetworkWithAzure

## Build the Azure IoT Edge Modules

Now that we have the neural network built, which consist of 5 files, we can build and push our two Azure IoT Edge Modules, one for aquiring the WAV file, one for inferencing the file.

You can find the Build Edge Modules script in samples\4-buildEdgeModules

## Deploy the Edge Module to the VAI DevKit

Finally, with the model and Edge Modules built, we can deploy to our VAI DevKit.

You can find the deploy script in samples\5-deployEdgeModules
