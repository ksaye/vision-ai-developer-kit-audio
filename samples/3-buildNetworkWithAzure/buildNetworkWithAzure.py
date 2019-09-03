# pip install azureml-core azureml-train azureml-contrib-iot azure-mgmt-containerregistry azure-cli

import os
import sys
import shutil
import datetime
import time
import azureml
import azureml.core
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core.container_registry import ContainerRegistry
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.datastore import Datastore
from azureml.core.runconfig import DataReferenceConfiguration, MpiConfiguration, TensorflowConfiguration
from azureml.train.dnn import TensorFlow

# change these variables as needed
azureSubscriptionID = 'dc6f7REMOVED46722'
azureResourceGroup = 'audioRG'
azureMLWorkSpaceName = 'audioWorkSpace'
azureMLWorkSpaceLocation = "South Central US"
azureMLClusterName = "cluster3"
azureMLVMSize = 'Standard_NC6' # consider 'Standard_D2', 'Standard_NC6' or 'STANDARD_D14'
azureMLMazNodes = 1
experiment_name = 'KerasAudioExperiment'
azureStorgeAccountName = 'kevinsayazstorage'
azureStorageKeyName = '8H5YxVfREMOVEDvaXvHgxiA=='
azureStorageTargetContainer = 'newfolder'
# end of change section

# if we don't have a workspace, authenticate the user and create one
if azureMLWorkSpaceName not in Workspace.list(subscription_id=azureSubscriptionID):
    ws=Workspace.create(subscription_id=azureSubscriptionID, resource_group=azureResourceGroup, name=azureMLWorkSpaceName, location=azureMLWorkSpaceLocation)
else:
    ws=Workspace.get(azureMLWorkSpaceName, subscription_id=azureSubscriptionID)

# create or use an existing experiment
exp = Experiment(workspace=ws, name=experiment_name)

# register our existing Azure Blob Container with the labled audio files
ds = Datastore.register_azure_blob_container(workspace=ws, datastore_name=azureStorageTargetContainer, container_name=azureStorageTargetContainer,
    account_name=azureStorgeAccountName, account_key=azureStorageKeyName, create_if_not_exists=False)

# create a reference where we mount the DataStore to the container instance
dr = DataReferenceConfiguration(datastore_name=ds.name, path_on_compute='data', mode='mount')

# upload any needed files
ws.get_default_datastore().upload(src_dir='.', target_path='.', overwrite=True, show_progress=True)

# create the computer_target object, if it does not exist
try:
    compute_target = ComputeTarget(workspace=ws, name=azureMLClusterName)
    print('using existing computer cluster: ' + azureMLClusterName)
except ComputeTargetException:
    print('Creating a new compute target: ' + azureMLClusterName)
    compute_config = AmlCompute.provisioning_configuration(vm_size=azureMLVMSize, vm_priority='lowpriority', max_nodes=azureMLMazNodes, 
        idle_seconds_before_scaledown=600, admin_username=azureMLClusterName[:8].lower(), admin_user_password=azureStorageKeyName[:20])
    compute_target = ComputeTarget.create(workspace=ws, name=azureMLClusterName, provisioning_configuration=compute_config)
    compute_target.wait_for_completion(show_output=True, timeout_in_minutes=20)

script_params = {
    '--data_dir': ds.as_mount()
}

# using a TensorFlow estimator so we can parallel execute
est = TensorFlow(source_directory='.',
                 entry_script='run.py',
                 script_params=script_params,
                 compute_target=compute_target,
                 pip_packages=['keras==2.2.5', 'sklearn', 'librosa==0.7.0', 'lru-dict==1.1.6', 'azure-storage'],
                 use_gpu=("NC" in azureMLVMSize.upper()),
                 framework_version='1.13',
                 node_count=azureMLMazNodes,
#   for production stuff, use a custom docker image instead of the 'os.system' lines in run.py
#                 custom_docker_image=ContainerRegistry(address="a", username="b", password="c"),
                 process_count_per_node=1,
                 distributed_training=MpiConfiguration())

run = exp.submit(est)

run.wait_for_completion(show_output=True)

model = run.register_model(model_name=experiment_name, 
                            model_path='outputs/model',
                            description=experiment_name + ' built on ' + str(azureMLMazNodes) + ' nodes of ' + azureMLVMSize + ' from ' + azureStorgeAccountName + '/' + azureStorageTargetContainer)

# downloading the files for the build step or pull it from the Azure Blob Storage
run.download_file(name='outputs/model/cifar10-architecture.json', output_file_path ='../4-buildEdgeModules/audioinference/models/cifar10-architecture.json')
run.download_file(name='outputs/model/cifar10-config.npy', output_file_path ='../4-buildEdgeModules/audioinference/models/cifar10-config.npy')
run.download_file(name='outputs/model/cifar10-history.npy', output_file_path ='../4-buildEdgeModules/audioinference/models/cifar10-history.npy')
run.download_file(name='outputs/model/cifar10-weights.h5', output_file_path ='../4-buildEdgeModules/audioinference/models/cifar10-weights.h5')
