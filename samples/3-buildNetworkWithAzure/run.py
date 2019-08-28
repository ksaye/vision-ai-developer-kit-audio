import os
import sys
import shutil
import argparse

os.system('apt update && apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev portaudio19-dev')
os.system('git clone https://github.com/chen0040/keras-audio.git')
os.system('cp -r keras-audio/keras_audio .')
os.system('mkdir model')

sys.path.append('.')
from azure.storage.blob import BlockBlobService
from keras_audio.library.cifar10 import Cifar10AudioClassifier

azureStorgeAccountName = 'kevinsayazstorage'
azureStorageKeyName = 'dMCtO9WjChghiRc7OGw=='
azureStorageContainer = 'completedmodel'
parser = argparse.ArgumentParser()
parser.add_argument("--data_dir")
args = parser.parse_args()

def load_path_labels(sourcePath):
    # here we are expecting file in the format XXXXXXX-N.wav, where N is the label
    pairs = []
    for f in os.listdir(sourcePath):
        try:
            if f.split('.')[1] == 'wav':                           # only process wav files
                label = f.split('.')[0].split('-')[1]
                path = sourcePath + '/' + f
                lableCounter = (int(label)/10) - 1
                pairs.append((path, lableCounter))
        except:
            print('error with: ' + str(f))
    return pairs
 
def main():
    block_blob_service = BlockBlobService(account_name=azureStorgeAccountName, account_key=azureStorageKeyName)
    if (block_blob_service.exists(container_name=azureStorageContainer) == False):
        block_blob_service.create_container(container_name=azureStorageContainer)

    audio_path_label_pairs = load_path_labels(str(args.data_dir))
    print('loaded: ' + str(len(audio_path_label_pairs)) + ' files')
 
    classifier = Cifar10AudioClassifier()
    batch_size = 8
    epochs = 20000
    classifier.fit(audio_path_label_pairs=audio_path_label_pairs, model_dir_path='model', batch_size=batch_size, epochs=epochs)

    #zipping and uploading the compiled model to blob storage
    shutil.make_archive(base_name='model.zip', format='zip', base_dir='model')
    block_blob_service.create_blob_from_path(azureStorageContainer, 'model.zip', 'model.zip')
 
if __name__ == '__main__':
    main()
