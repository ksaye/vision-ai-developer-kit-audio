# Labeling Sample Audio Files

This python file copies files from one Azure Blob Storage container to another labeling the file in the format NNNNNNN-XX.WAV, where XX is the lable.

For our sample, we use the labels 100, 90, 80 and so on.

## Configuring the script

In 2-labelFiles\labelFiles.py make the following modification

Setting | Example | Notes
------- | ------- | --------
azureStorgeAccountName | 'myaudiostorgeaccount' | the name of your Azure Blob Storge Account.  it must match the setting used in 1-audioAquisition
azureStorageKeyName | 'dMCtO97OGw==' | the primary or secondary key of your Azure Blob Storage Account
azureStorageSourceContainer | 'newfountain' | the source Blob container in the storage account.  it must match the setting used in 1-audioAquisition
azureStorageTargetContainer | 'newfolder5' | the target Blob container
emptyTargetContainer | True | should all files in the target container be deleted
labels | [100,90,80,70,60,50,40,30,20,10] | the labels of the files

## Running the script

at a command prompt run:
```bash
python lableFiles.py
```

or in Visual Studio Code with the file open, right click in the center of the Editor window and select Run Python File in Terminal

The script can take a while to copy and label files.  Every 100 files you should see a '.' on the screen.
