# based off: https://kevinsaye.wordpress.com/2018/11/01/audio-classification-training-in-23-lines-of-code/ which includes
import time, os, sys, datetime
from azure.storage.blob import BlockBlobService

# change these variables as needed
azureStorgeAccountName = 'kevinsayazstorage'
azureStorageKeyName = 'dMCtO9kFWjChghiRc7OGw=='
azureStorageContainer = 'kevindemo'
fileStorageLocation = '/'
sampleStartHour = 0
sampleEndHour = 24
delayBetweenSampleSeconds = 60
lengthOfAudioSampleSeconds = 15
# end of change section

def main():
    # setting up the environment and increasing the microphone volume
    os.system("amixer cset name='AIF1_CAP Mixer SLIM TX5' 1")
    os.system("amixer cset name='AIF1_CAP Mixer SLIM TX6' 1")
    os.system("amixer cset name='AIF1_CAP Mixer SLIM TX7' 1")
    os.system("amixer cset name='AIF1_CAP Mixer SLIM TX8' 1")
    os.system("amixer cset name='SLIM_0_TX Channels' 'Four'")
    os.system("amixer cset name='CDC_IF TX5 MUX' 'DEC5'")
    os.system("amixer cset name='ADC MUX5' 'DMIC'")
    os.system("amixer cset name='DMIC MUX5' 'DMIC0'")
    os.system("amixer cset name='CDC_IF TX6 MUX' 'DEC6'")
    os.system("amixer cset name='ADC MUX6' 'DMIC'")
    os.system("amixer cset name='DMIC MUX6' 'DMIC1'")
    os.system("amixer cset name='CDC_IF TX7 MUX' 'DEC7'")
    os.system("amixer cset name='ADC MUX7' 'DMIC'")
    os.system("amixer cset name='DMIC MUX7' 'DMIC2'")
    os.system("amixer cset name='CDC_IF TX8 MUX' 'DEC8'")
    os.system("amixer cset name='ADC MUX8' 'DMIC'")
    os.system("amixer cset name='DMIC MUX8' 'DMIC3'")
    os.system("amixer cset name='DEC5 Volume' 124")     # the volume is from 0 - 124
    os.system("amixer cset name='DEC6 Volume' 124")     # the volume is from 0 - 124
    os.system("amixer cset name='DEC7 Volume' 124")     # the volume is from 0 - 124
    os.system("amixer cset name='DEC8 Volume' 124")     # the volume is from 0 - 124
    os.system("amixer cset name='MultiMedia1 Mixer SLIM_0_TX' 1")

    block_blob_service = BlockBlobService(account_name=azureStorgeAccountName, account_key=azureStorageKeyName)

    # create the azureStorageContainer if it does not exist
    if (block_blob_service.exists(container_name=azureStorageContainer) == False):
        block_blob_service.create_container(container_name=azureStorageContainer)

    while(True):
        try:
            if datetime.datetime.now().hour >= sampleStartHour and datetime.datetime.now().hour <= sampleEndHour:
                os.system('if [ -f ' + fileStorageLocation + '*.wav ] ; then rm ' + fileStorageLocation + '*.wav ; fi')
                fileOnly = time.strftime('%Y-%m-%d-%H-%M-%S') + '.wav'
                filename = fileStorageLocation + fileOnly
                os.system('arecord -d 10 --duration=' + str(lengthOfAudioSampleSeconds) + ' -f cd -vv ' + filename)
                block_blob_service.create_blob_from_path(azureStorageContainer, fileOnly, filename)
                os.remove(filename)
                time.sleep(delayBetweenSampleSeconds)
        except:
            e = sys.exc_info()[0]
            print ( "Unexpected error: %s" % e )

if __name__ == '__main__':
    main()
