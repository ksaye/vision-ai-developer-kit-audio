# Using Azure Machine Learning Workspace, train the Model

# Overview

This step uses Azure Machine Learning Workspace to remotely build the model based on the labled files in the Azure Blob Storage Account.

The script performs the following items:
1. Creates the Azure Machine Learning Workspace
2. Creates the Compute resources and Compute to Azure Blob Storage connection
3. Configures the Compute resource with the needed Python packages
4. Runs the 'run.py' file, which computes a 'mel-spectrogram' for each file and finally trains the model

## Configuring the script

In 3-buildNetworkWithAzure\buildNetworkWithAzure.py make the following modification:

Setting | Example | Notes
------- | ------- | --------
azureSubscriptionID | 'dc6f773e-4b13-4f8b-8d76-f34469246722' | the azure Subscription ID
azureResourceGroup | 'audioRG' | the resource group to create the WorkSpace
azureMLWorkSpaceName | 'audioWorkSpace' | the Azure Machine Learning Workspace name
azureMLWorkSpaceLocation | "South Central US" | the Region for the Azure Machine Learning Workspace
azureMLClusterName | "cluster3" | the name of the compute cluster
azureMLVMSize | 'Standard_D14' | the SKU or size of the compute VMs
azureMLMaxNodes | 4 | the max number of nodes to use
experiment_name | 'KerasAudioExperiment' | the name of the experiment
azureStorgeAccountName | 'myaudiostorgeaccount' | the name of your Azure Blob Storge Account.  it must match the setting used in 1-audioAquisition
azureStorageKeyName | 'dMCtO9iRc7OGw==' | the primary or secondary key of your Azure Blob Storage Account
azureStorageTargetContainer | 'newfolder5' | the target Blob container.  it must match the setting used in 2-labelFiles


In 3-buildNetworkWithAzure\run.py make the following modification

Setting | Example | Notes
------- | ------- | --------
azureStorgeAccountName | 'myaudiostorgeaccount' | the name of your Azure Blob Storge Account.  it must match the setting used in 1-audioAquisition
azureStorageKeyName | 'dMCtO9kRc7OGw==' | the primary or secondary key of your Azure Blob Storage Account
azureStorageContainer | 'completedmodel' | the name of the Azure Storage Blob container for the trained model (zip file)

## Running the script

at a command prompt run:
```bash
# install the required Python libraries
pip install azureml-core azureml-contrib-iot azure-mgmt-containerregistry azure-cli

python buildNetworkWithAzure.py
```

or in Visual Studio Code with the file open, right click in the center of the Editor window and select Run Python File in Terminal