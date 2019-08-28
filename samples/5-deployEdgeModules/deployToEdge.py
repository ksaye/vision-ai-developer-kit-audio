import os

# change these variables as needed
azureIoTHubName = 'viadevkit1'
azureIoTHubDeviceName = 'visionaidkit'
azureSubscriptionID = 'dc6f773e-4b13-4f8b-8d76-f34469246722'
ContainerRegistryName = 'kevinsay.azurecr.io'
ContainerRegistryUserName = 'kevinsay'
ContainerRegistryPassword = 'HN11kh8fB'
# end of change section

file = open('./deployment.json')
contents = file.read()
contents = contents.replace('__REGISTRY_NAME', ContainerRegistryName.split('.')[0])
contents = contents.replace('__REGISTRY_USER_NAME', ContainerRegistryUserName)
contents = contents.replace('__REGISTRY_PASSWORD', ContainerRegistryPassword)
contents = contents.replace('__IMAGECAPTUREMODULE_URL', ContainerRegistryName + '/' + 'imagecapture')
contents = contents.replace('__IMAGECAPTUREMODULE_NAME', 'imagecapture')
contents = contents.replace('__IMAGEINFERENCEMODULE_URL', ContainerRegistryName + '/' + 'imageinference')
contents = contents.replace('__IMAGEINFERENCEMODULE_NAME', 'imageinference')
with open('./deployment.json', 'wt', encoding='utf-8') as output_file:
    output_file.write(contents)

os.system('az login')
os.system('az account set --subscription "' + azureSubscriptionID + '"')
os.system('az extension add --name azure-cli-iot-ext')
os.system('az iot edge set-modules --device-id '+ azureIoTHubDeviceName + ' --hub-name '+ azureIoTHubName + ' --content deployment.json')