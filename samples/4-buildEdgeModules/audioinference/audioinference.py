import os, sys, time, json
from datetime import datetime
sys.path.append('.')
from keras_audio.library.cifar10 import Cifar10AudioClassifier  
from flask import Flask, request
from keras import backend as K

port=8080
labels = [100,90,80,70,60,50,40,30,20,10]
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024

# removing any old files
try:
    os.remove('*.wav')
    os.remove('*.wav-mg.npy')
except:
    print ( 'no old files to remove' )

@app.route('/', methods=['POST', 'GET'])
def index():
    request_file = None
    try:
        request_file = request.files['file']
    except:
        print ('Error: ' + str(sys.exc_info()[0]))

    print ('Success: Received file: ' + request_file.filename)
    request_file.save(request_file.filename)
    responseJSON = processFile(request_file.filename)
    print (responseJSON)
    return responseJSON

def processFile(filename):
    classifier = Cifar10AudioClassifier()
    classifier.load_model(model_dir_path='./models')
    predicted_label_id = classifier.predict_class(filename)
    predicted_label = labels[predicted_label_id]
    predicted_scores = classifier.predict(filename)
    predicted_score = predicted_scores[predicted_label_id]

    data = {}
    data['label'] = predicted_label
    data['score'] = float(predicted_score)
    data['dateTime'] =  str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data['modelDate'] = str(time.ctime(os.path.getmtime('models/cifar10-weights.h5')))
    data['fileProcessed'] = filename

    os.remove(filename + "-mg.npy")
    os.remove(filename)
    K.clear_session()
    return json.dumps(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
