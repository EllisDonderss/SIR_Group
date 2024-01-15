import json
import math
import numpy as np

from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, Dialogflow, GetIntentRequest, QueryResult, RecognitionResult)

mode_dict = {'submissive': "\\rspd=50\\\\vct=150\\\\vol=40\\", 'neutral': "\\rspd=100\\\\vct=100\\\\vol=60\\", 'dominant': "\\rspd=150\\\\vct=50\\\\vol=80\\"}


def calculate_ammount(amount):
    ''' Calculates the amount of cookies that will be returned to the user by the Nao robot. '''
    return int(math.ceil(int(amount) * 2 / 3))

def game_start(nao):
    voice_mode_dict = mode_dict["dominant"]
    # the callback function
    def on_dialog(message):
        if message.response:
            if message.response.recognition_result.is_final:
                print("Transcript:", message.response.recognition_result.transcript)

    # load the key json file
    keyfile_json = json.load(open("my-project-1546018025994-c8e7e22cf98c.json"))

    # set up the config
    conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

    # initiate Dialogflow object
    dialogflow = Dialogflow(ip='localhost', conf=conf)


    # register a callback function to act upon arrival of recognition_result
    dialogflow.register_callback(on_dialog)

    # Demo starts
    nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + "So, how much would you like to give me?"))
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
                # Get the amount
                amount = reply.response.query_result.parameters["number"]
                print(amount)
                calculated_amount = calculate_ammount(amount)
                # Speak the response
                nao.tts.request(NaoqiTextToSpeechRequest(f"I will give you 2/3 of {amount} which is {calculated_amount}"))
            nao.tts.request(NaoqiTextToSpeechRequest(voice_mode_dict + text))