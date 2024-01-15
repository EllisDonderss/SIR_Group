import json
import numpy as np

from submissive_demo import act_submissive
from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, GetIntentRequest, RecognitionResult,
                                                          QueryResult, Dialogflow)

""" 
This demo should have Nao picking up your intent and replying according to your trained agent using dialogflow.

The Dialogflow should be running. You can start it with:
[services/dialogflow] python dialogflow.py
"""

# the callback function
def on_dialog(message):
    if message.response:
        if message.response.recognition_result.is_final:
            print("Transcript:", message.response.recognition_result.transcript)

# connect to the robot
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

# Demo starts
nao.tts.request(NaoqiTextToSpeechRequest("\\vct=50\\Hello, my name is NAO and who are you?"))
print(" -- Ready -- ")
x = np.random.randint(10000)

pepernoten = 10

def game_init(value):
    return value + pepernoten


def start_acting():
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


for i in range(25):
    print(" ----- Conversation turn", i)
    reply = dialogflow.request(GetIntentRequest(x))
    print(45*"-")
    print(reply.intent)
    print(45*"-")
    if reply.fulfillment_message:
        text = reply.fulfillment_message
        print("Reply:", text)
        print(reply)

        # if reply.intent == "nao_game_instructions":
        #     act_submissive()

        nao.tts.request(NaoqiTextToSpeechRequest(text))
