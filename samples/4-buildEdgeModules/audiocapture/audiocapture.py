import time, os, sys, datetime, requests, json
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubModuleClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError

# change these variables as needed
fileStorageLocation = '/'
sampleStartHour = 0
sampleEndHour = 24
delayBetweenSampleSeconds = 60
lengthOfAudioSampleSeconds = 15
# end of change section

# messageTimeout - the maximum time in milliseconds until a message times out.
# The timeout period starts at IoTHubModuleClient.send_event_async.
# By default, messages do not expire.
MESSAGE_TIMEOUT = 10000

# global counters
RECEIVE_CALLBACKS = 0
SEND_CALLBACKS = 0

# Choose HTTP, AMQP or MQTT as transport protocol.  Currently only MQTT is supported.
PROTOCOL = IoTHubTransportProvider.MQTT

# Callback received when the message that we're forwarding is processed.
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "    Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_CALLBACKS )

class HubManager(object):

    def __init__(
            self,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubModuleClient()
        self.client.create_from_environment(protocol)

        # set the time until a message times out
        self.client.set_option("messageTimeout", MESSAGE_TIMEOUT)

    # Forwards the message received onto the next stage in the process.
    def forward_event_to_output(self, outputQueueName, event, send_context):
        self.client.send_event_async(
            outputQueueName, event, send_confirmation_callback, send_context)

def main(protocol):
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

    hub_manager = HubManager(protocol)

    while(True):
        try:
            if datetime.datetime.now().hour >= sampleStartHour and datetime.datetime.now().hour <= sampleEndHour:
                os.system('if [ -f ' + fileStorageLocation + '*.wav ] ; then rm ' + fileStorageLocation + '*.wav ; fi')
                fileOnly = time.strftime('%Y-%m-%d-%H-%M-%S') + '.wav'
                filename = fileStorageLocation + fileOnly
                os.system('arecord -d 10 --duration=' + str(lengthOfAudioSampleSeconds) + ' -f cd -vv ' + filename)
                response = json.loads(requests.post('http://audioinference:8080/', files={'file': open(filename, 'rb')}).text)
                hub_manager.forward_event_to_output('output1', response, SEND_CALLBACKS)
                os.remove(filename)
                time.sleep(delayBetweenSampleSeconds)
        except:
            e = sys.exc_info()[0]
            print ( "Unexpected error: %s" % e )

if __name__ == '__main__':
    main(PROTOCOL)
