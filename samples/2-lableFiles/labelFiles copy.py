import sys
from azure.storage.blob import BlockBlobService

# change these variables as needed
azureStorgeAccountName = 'kevinsayazstorage'
azureStorageKeyName = 'dMCtO9kFJ7u0VJq6638ZY4uokBW1PaF30CfKg/Ig81GFpyVDIlhELYWz6XaAKcUIemQl1l++cWjChghiRc7OGw=='
azureStorageContainer = 'fountain'
azureStorageTargetContainer = 'newfolder2'
emptyTargetContainer = True
maxFiles = 50000
labels = [100,90,80,70,60,50,40,30,20,10]
# end of change section

def main():
    sourceBlobCounter=0
    currentBlobCounter=0
    currentLabel=None
    block_blob_service = BlockBlobService(account_name=azureStorgeAccountName, account_key=azureStorageKeyName)
    block_blob_generator = block_blob_service.list_blobs(azureStorageContainer, num_results=maxFiles)

    # create the TargetContainer if it does not exist
    if (block_blob_service.exists(azureStorageTargetContainer) == False):
        block_blob_service.create_container(azureStorageTargetContainer)
        print('created target container: ' + azureStorageTargetContainer)
    elif emptyTargetContainer:
        print('deleting existing files in the container: ' + azureStorageTargetContainer)
        for toDelete in block_blob_service.list_blobs(azureStorageTargetContainer, num_results=maxFiles):
            block_blob_service.delete_blob(azureStorageTargetContainer, toDelete.name)

    print('counting files in the source container: ' + azureStorageContainer)
    for blob in block_blob_generator:
        sourceBlobCounter +=1

    print('copying and labeling ' + str(sourceBlobCounter) + ' files to container: ' + azureStorageTargetContainer)
    block_blob_generator = block_blob_service.list_blobs(azureStorageContainer, num_results=maxFiles)
    for blob in block_blob_generator:
        sourceBlob = block_blob_service.make_blob_url(azureStorageContainer, blob.name)
        label = labels[int((currentBlobCounter/sourceBlobCounter) * len(labels))]
        targetName = blob.name.split('.')[0].replace('-', '_') + '-' + str(label) + '.' + blob.name.split('.')[1]
        block_blob_service.copy_blob(azureStorageTargetContainer, targetName, sourceBlob)
        if currentLabel != label:
            print("FileNumber: " + str(currentBlobCounter)+ " begins label: " + str(label))
            currentLabel = label
#        sys.stdout.write('.')
#        sys.stdout.flush()
        currentBlobCounter+=1

if __name__ == '__main__':
    main()