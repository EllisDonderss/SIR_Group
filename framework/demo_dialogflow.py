import json
import numpy as np
import final_dominant
import math

from submissive_demo import act_submissive

from sic_framework.devices import Nao
from sic_framework.devices.desktop import Desktop
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, GetIntentRequest, RecognitionResult,
                                                          QueryResult, Dialogflow)

from argparse import ArgumentParser
""" 
This demo should have Nao picking up your intent and replying according to your trained agent using dialogflow.

The Dialogflow should be running. You can start it with:
[services/dialogflow] python dialogflow.py
"""
parser = ArgumentParser()

parser.add_argument('-M', '--mode',
                dest='mode',
                help='Which mode to use. [dominant, submissive, neutral]',
                default='neutral', type=str)
args = parser.parse_args()

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

mode_dict = {'submissive': "\\rspd=70\\\\vct=115\\\\vol=90\\", 'neutral': "\\rspd=100\\\\vct=100\\\\vol=80\\", 'dominant': "\\rspd=100\\\\vct=50\\\\vol=100\\"}

cookie_ammount = 5

def calculate_ammount(amount):
    return int(math.ceil(((int(amount) * 2) + cookie_ammount) * 2/3))

def dialogflow_start(nao, use_desktop_microphone=True):
    voice_mode_dict = mode_dict["dominant"]
    # the callback function
    def on_dialog(message):
        if message.response:
            if message.response.recognition_result.is_final:
                print("Transcript:", message.response.recognition_result.transcript)


    keyfile_json = json.load(open("my-project-1546018025994-c8e7e22cf98c.json"))
    # load the key json file
    if use_desktop_microphone:
        conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=44100, language="en")
    else:
        # set up the config
        conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

    # initiate Dialogflow object
    dialogflow = Dialogflow(ip='localhost', conf=conf)

    # connect the output of NaoqiMicrophone as the input of DialogflowComponent
    if use_desktop_microphone:
        desktop = Desktop()
        dialogflow.connect(desktop.mic)
    else:
        dialogflow.connect(nao.mic)

    # register a callback function to act upon arrival of recognition_result
    dialogflow.register_callback(on_dialog)

    # Demo starts
    nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + "Hello, my name is NAO and who are you? "))
    print(" -- Ready -- ")
    x = np.random.randint(10000)
    for i in range(25):
        print(" ----- Conversation turn", i)
        reply = dialogflow.request(GetIntentRequest(x))

        print(reply.intent)

        # new_ammount = game_init(reply)

        if reply.fulfillment_message:
            text = reply.fulfillment_message
            print("Reply:", text)
            if reply.intent == "nao_game_collection":
                nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + text))
                # Get the amount
                amount = reply.response.query_result.parameters["number"]
                print(amount)
                calculated_amount = calculate_ammount(amount)
                # Speak the response
                print(calculated_amount)
                nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + f"I will give you two thirds of {amount} which is {calculated_amount}. This was fun, thank you for participating. Please talk to my caretaker for filling out a survey"))
            nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + text))


dialogflow_start(nao)