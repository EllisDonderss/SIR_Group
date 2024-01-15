import json
import numpy as np
from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, GetIntentRequest)
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest, NaoqiBreathingRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest
from sic_framework.devices.common_naoqi.naoqi_autonomous import (
    NaoWakeUpRequest,
    NaoRestRequest,
    NaoBasicAwarenessRequest
)
from sic_framework.devices.nao import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, Dialogflow, GetIntentRequest, QueryResult, RecognitionResult)


def on_dialog(message):
    if message.response and message.response.recognition_result.is_final:
        print("Transcript:", message.response.recognition_result.transcript)

def give_pepernoten(amount):
    return int(int(amount) * 2 / 3)

# Connect to the robot
nao = Nao(ip='192.168.0.242')

# Load the key json file
keyfile_json = json.load(open("new-dnng-b0df09ad97ef.json"))

# Set up the config
conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

# Initiate Dialogflow object
dialogflow = Dialogflow(ip='localhost', conf=conf)

# Connect the output of NaoqiMicrophone as the input of DialogflowComponent
dialogflow.connect(nao.mic)

# Register a callback function to act upon arrival of recognition_result
dialogflow.register_callback(on_dialog)

# Demo starts
nao.tts.request(NaoqiTextToSpeechRequest("Hello! Do you want to play a game?"))
print(" -- Ready -- ")
x = np.random.randint(10000)

for i in range(25):
    print(" ----- Conversation turn", i)
    reply = dialogflow.request(GetIntentRequest(123))
    print(45 * "-")
    print(reply.intent)
    print(45 * "-")
    if reply.fulfillment_message:
        text = reply.fulfillment_message
        print("Reply:", text)        
        if reply.intent == "greetings":
            print(" -- MADE IT HERE -- ")
            nao.tts.request(NaoqiTextToSpeechRequest(text))
            # Ask for pepernoten
            #nao.tts.request(NaoqiTextToSpeechRequest("How many peppernoten do you want to give me?"))
            # Wait for the response
            reply = dialogflow.request(GetIntentRequest(123))
            if reply.intent == "number_given":
                print(" -- MADE IT HERE -- ")
                # Get the amount
                amount = reply.response.query_result.parameters["number"]
                print(amount)
                calculated_amount = give_pepernoten(amount)
                # Speak the response
                nao.tts.request(NaoqiTextToSpeechRequest(f"I will give you 2/3 of {amount} which is {calculated_amount}"))
            nao.tts.request(NaoqiTextToSpeechRequest(text))
        nao.tts.request(NaoqiTextToSpeechRequest(text))