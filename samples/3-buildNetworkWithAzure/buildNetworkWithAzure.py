# pip install azureml-core azureml-contrib-iot azure-mgmt-containerregistry azure-cli

import os
import sys
import shutil
import azureml
import azureml.core
from azureml.core import Workspace
from azureml.core import Run
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
from azureml.core import Environment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.datastore import Datastore
from azureml.core.environment import CondaDependencies
from azureml.core.runconfig import DataReferenceConfiguration, RunConfiguration

# change these variables as needed
azureSubscriptionID = 'dc69246722'
azureResourceGroup = 'audioRG'
azureMLWorkSpaceName = 'audioWorkSpace'
azureMLWorkSpaceLocation = "South Central US"
azureMLClusterName = "cluster3"
azureMLVMSize = 'Standard_D14'
experiment_name = 'KerasAudioExperiment'
azureStorgeAccountName = 'kevinsayazstorage'
azureStorageKeyName = 'dMCtO9kFJ7hiRc7OGw=='
azureStorageTargetContainer = 'newfolder5'
# end of change section

# if we don't have a workspace, authenticate the user and create one
if azureMLWorkSpaceName not in Workspace.list(subscription_id=azureSubscriptionID):
    ws=Workspace.create(subscription_id=azureSubscriptionID, resource_group=azureResourceGroup, name=azureMLWorkSpaceName, location=azureMLWorkSpaceLocation, )
else:
    ws=Workspace.get(azureMLWorkSpaceName, subscription_id=azureSubscriptionID)

# create an experiment
exp = Experiment(workspace=ws, name=experiment_name)

# register our existing Azure Blob Container with the labled audio files
ds = Datastore.register_azure_blob_container(workspace=ws, datastore_name=azureStorageTargetContainer, container_name=azureStorageTargetContainer,
    account_name=azureStorgeAccountName, account_key=azureStorageKeyName, create_if_not_exists=False)

# upload our source files
#ds.upload(src_dir='scripts', target_path='.',  overwrite=True, show_progress=True)

# create a reference where we mount the DataStore to the container instance
dr = DataReferenceConfiguration(datastore_name=ds.name, path_on_compute='data', mode='mount')

# create the computer_target object, if it does not exist
try:
    compute_target = ComputeTarget(workspace=ws, name=azureMLClusterName)
    print('using existing computer cluster: ' + azureMLClusterName)
except ComputeTargetException:
    print('Creating a new compute target: ' + azureMLClusterName)
    compute_config = AmlCompute.provisioning_configuration(vm_size=azureMLVMSize, max_nodes=1, idle_seconds_before_scaledown=600)
    compute_target = ComputeTarget.create(workspace=ws, name=azureMLClusterName, provisioning_configuration=compute_config)
    compute_target.wait_for_completion(show_output=True, timeout_in_minutes=20)

# configuring our custom run configuration
run_config = RunConfiguration(framework='python')
run_config.target = compute_target.name
run_config.environment.docker.enabled = True
run_config.data_references = {ds.name: dr}
run_config.environment.python.user_managed_dependencies = False
conda_dependencies = CondaDependencies()
conda_dependencies.add_pip_package('keras==2.2.5')         # adding pip packages
conda_dependencies.add_pip_package('tensorflow==1.14.0')   # adding pip packages
conda_dependencies.add_pip_package('sklearn')              # adding pip packages
conda_dependencies.add_pip_package('librosa==0.7.0')       # adding pip packages
conda_dependencies.add_pip_package('lru-dict==1.1.6')      # adding pip packages
conda_dependencies.add_pip_package('azure-storage')        # adding pip packages
run_config.environment.python.conda_dependencies = conda_dependencies

script_run_config = ScriptRunConfig(source_directory=".", run_config=run_config, script='run.py', arguments=['--data_dir', str(ds.as_mount())])

run = exp.submit(config=script_run_config)

run.wait_for_completion(show_output=True)

# downloading the files for the build step or pull it from the Azure Blob Storage
run.download_file(name='model/cifar10-architecture.json', output_file_path ='../4-buildEdgeModules/model')
run.download_file(name='model/cifar10-config.npy', output_file_path ='../4-buildEdgeModules/model')
run.download_file(name='model/cifar10-history.npy', output_file_path ='../4-buildEdgeModules/model')
run.download_file(name='model/cifar10-weights.h5', output_file_path ='../4-buildEdgeModules/model')
