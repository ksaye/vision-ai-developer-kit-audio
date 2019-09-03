import sys, datetime
from azure.storage.blob import BlockBlobService

# change these variables as needed
azureStorgeAccountName = 'kevinsayazstorage'
azureStorageKeyName = '8H5YxVREMOVEDHgxiA=='
azureStorageSourceContainer = 'fountainsample'
azureStorageTargetContainer = 'newfolder3'
emptyTargetContainer = True
labels = [100,90,80,70,60,50,40,30,20,10]
# end of change section

def main():
    sourceBlobCounter=0
    currentBlobCounter=0
    currentLabel=None
    block_blob_service = BlockBlobService(account_name=azureStorgeAccountName, account_key=azureStorageKeyName)

    # create the TargetContainer if it does not exist
    if (block_blob_service.exists(container_name=azureStorageTargetContainer) == False):
        block_blob_service.create_container(container_name=azureStorageTargetContainer)
        print(str(datetime.datetime.now()) + ': created target container: ' + azureStorageTargetContainer)
    elif emptyTargetContainer:
        print(str(datetime.datetime.now()) + ': deleting existing files in the container: ' + azureStorageTargetContainer)
        while True:
            delete_blob_generator = block_blob_service.list_blobs(container_name=azureStorageTargetContainer)
            for toDelete in block_blob_service.list_blobs(container_name=azureStorageTargetContainer):
                block_blob_service.delete_blob(container_name=azureStorageTargetContainer, blob_name=toDelete.name)
            if not delete_blob_generator.next_marker:
                break

    print(str(datetime.datetime.now()) + ': counting files in the source container: ' + azureStorageSourceContainer)
    while True:
        count_blob_generator = block_blob_service.list_blobs(container_name=azureStorageSourceContainer)
        for blob in count_blob_generator:
            sourceBlobCounter +=1
        if not count_blob_generator.next_marker:
            break

    print(str(datetime.datetime.now()) + ': copying and labeling ' + str(sourceBlobCounter) + ' files to container: ' + azureStorageTargetContainer)
    while currentBlobCounter < sourceBlobCounter:
        copy_blob_generator = block_blob_service.list_blobs(container_name=azureStorageSourceContainer)
        for blob in copy_blob_generator:
            sourceBlob = block_blob_service.make_blob_url(container_name=azureStorageSourceContainer, blob_name=blob.name)
            label = labels[int((currentBlobCounter/sourceBlobCounter) * len(labels))]
            targetName = blob.name.split('.')[0].replace('-', '_') + '-' + str(label) + '.' + blob.name.split('.')[1]
            block_blob_service.copy_blob(container_name=azureStorageTargetContainer, blob_name=targetName, copy_source=sourceBlob)
            if currentLabel != label:
                print(str(datetime.datetime.now()) + ": file number: " + str(currentBlobCounter)+ " begins label: " + str(label))
                currentLabel = label
            if (currentBlobCounter % 100 == 0):
                sys.stdout.write('.')
                sys.stdout.flush()
            currentBlobCounter+=1
        if not copy_blob_generator.next_marker:
            break

if __name__ == '__main__':
    main()