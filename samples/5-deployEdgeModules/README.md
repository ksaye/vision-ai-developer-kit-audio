# Deploy Edge Modules to the VAI DevKit

## Overview

This is the final step where the new modules are pushed from the Container Registry to the VAI DevKit.

While this is much simpler with Visual Studio Code and the IoT Edge Extension, this step is part of a larger sample solution, so we will just run a Python script.

## Assumptions

1. You have already pushed Azure IOT Edge and modules the the VAI DevKit
2. You have an existing Azure IoT Hub


## Configuring the script

In 5-deployEdgeModules\deployToEdge.py make the following modification:

Setting | Example | Notes
------- | ------- | --------
azureIoTHubName | 'viadevkit1' | the name of your Azure IoT Hub
azureIoTHubDeviceName | 'visionaidkit' | the name of your IoT Edge device that is registered
azureSubscriptionID | 'dc6f773e-4b13-4f8b-8d76-f34469246722' | your Azure subscription id
ContainerRegistryName | 'kevinsay.azurecr.io' | your Container Registry must be the same referenced in step 4
ContainerRegistryUserName | 'kevinsay' | your Container Registry Username must be the same referenced in step 4
ContainerRegistryPassword | 'HN11cJ4kh8fB' | your Container Registry Password must be the same referenced in step 4

## Running the script 

```bash
cd samples\5-deployEdgeModules
python deployToEdge.py
```