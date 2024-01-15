import json
import numpy as np
import math
from sic_framework.devices.desktop import Desktop
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, Dialogflow, GetIntentRequest, QueryResult, RecognitionResult)

mode_dict = {'submissive': "\\rspd=70\\\\vct=115\\\\vol=80\\", 'dominant': "\\rspd=100\\\\vct=50\\\\vol=100\\"}

cookie_ammount = 5

def calculate_ammount(amount):
    amount = int(amount) * 2
    amount = amount + cookie_ammount
    return [amount, int(math.ceil(amount * 2/3))]

def dialogflow_start(placeholder, nao, use_desktop_microphone=False):
    voice_mode_dict = mode_dict["dominant"]
    # the callback function
    def on_dialog(message):
        if message.response:
            if message.response.recognition_result.is_final:
                print("Transcript:", message.response.recognition_result.transcript)

    # load the key json file
    keyfile_json = json.load(open("valiant-pager-366223-a6ea3692342c.json"))

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
    nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + "Hello, what is your name"))
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
                nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + f"I will give you two thirds of {calculated_amount[0]} which is {calculated_amount[1]}. Thank you for participating. Please talk to my caretaker for filling out a survey"))
            nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + text))