import time

from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import StartRecording, StopRecording, PlayRecording, NaoqiMotionRecorderConf, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices.nao import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, GetIntentRequest, RecognitionResult,
                                                          QueryResult, Dialogflow)

from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest
import json
from sic_framework.devices.common_naoqi.naoqi_leds import NaoLEDRequest, NaoFadeRGBRequest
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_autonomous import (NaoWakeUpRequest, NaoBlinkingRequest,
                                                                 NaoSpeakingMovementRequest, NaoRestRequest,
                                                                 NaoBasicAwarenessRequest, NaoListeningMovementRequest,
                                                                 NaoBackgroundMovingRequest)



# the callback function
def on_dialog(message):
    if message.response:
        if message.response.recognition_result.is_final:
            print("Transcript:", message.response.recognition_result.transcript)


# get ip key from json ip_key.json file
with open('ip_key.json') as f:
    data = json.load(f)

ip_key = data['ip_key']

nao = Nao(ip_key)

# load the key json file
keyfile_json = json.load(open("valiant-pager-366223-a6ea3692342c.json"))

# set up the config
conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

# initiate Dialogflow object
dialogflow = Dialogflow(ip='localhost', conf=conf)

# connect the output of NaoqiMicrophone as the input of DialogflowComponent
dialogflow.connect(nao.mic)

# register a callback function to act upon arrival of recognition_result
dialogflow.register_callback(on_dialog)

pepernoten = 10

def game_start(nao):
    nao.tts.request(NaoqiTextToSpeechRequest(f"I have {pepernoten} chocolates, how much would you like to invest?"))
    for i in range(3):
        print(" ----- Conversation turn", i)
        reply = dialogflow.request(GetIntentRequest(x))

        print(reply.intent)

        # new_ammount = game_init(reply)

        if reply.fulfillment_message:
            text = reply.fulfillment_message
            print("Reply:", text)
            nao.tts.request(NaoqiTextToSpeechRequest(text))

def act_submissive():
    # 1. starting stance
    nao.motion.request(NaoPostureRequest("Crouch", .5))

    # 3. blue lights
    nao.leds.request(NaoFadeRGBRequest("AllLeds", 0, 0, 1, 0))

    # 2. dominant gestures
    #   a. submissive position
    recording = NaoqiMotionRecording.load("gestures/submissive/submissive.motion")
    nao.motion_record.request(PlayRecording(recording))

    for i in range(25):
        game_start()


    print("Done with submissive position ")

    # go to neutral poition
    nao.motion.request(NaoPostureRequest("Crouch", .5))
    nao.autonomous.request(NaoRestRequest())

    nao.tts.request(NaoqiTextToSpeechRequest(text))
    nao.buttons.register_callback(start_acting())
    
