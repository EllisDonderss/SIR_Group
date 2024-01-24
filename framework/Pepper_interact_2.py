import json
import numpy as np
import math
import random
import time
import threading

from sic_framework.core.utils import is_sic_instance
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, \
    GetIntentRequest, RecognitionResult, QueryResult, Dialogflow
from sic_framework.services.webserver.webserver_pepper_tablet import Webserver, HtmlMessage, WebserverConf, TranscriptMessage, ButtonClicked
from sic_framework.devices.common_naoqi.pepper_tablet import NaoqiTablet, UrlMessage
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from sic_framework.devices import Pepper
from sic_framework.devices.nao import NaoqiTextToSpeechRequest, NaoqiMoveRequest, NaoqiAnimationRequest, NaoqiMotionActuator
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, GetIntentRequest, Dialogflow, RecognitionResult, QueryResult
from sic_framework.core import *

# Connect to the robot
nao = Pepper(ip='10.0.0.164')

# Load the key json file
keyfile_json = json.load(open("sirproject2024-2-85be5a91ffe7.json"))

# Set up the Dialogflow config
conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

# Initiate Dialogflow object
dialogflow = Dialogflow(ip='localhost', conf=conf)

port = 8080

# images to display on the tablet
web_url_low_battery = f'https://publicdomainvectors.org/photos/Battery-4-2016101425.png'
web_url_T1
web_url_T2
web_url_T3
web_url_T4
web_url_T5

# images to display on the tablet when giving back money
web_url_T2_back
web_url_T3_back
web_url_T4_back
web_url_T5_back

#web_url_half_battery = f'https://publicdomainvectors.org/photos/Battery-3-2016101425.png'
#web_url_full_battery = f'https://publicdomainvectors.org/photos/Battery-2-2016101425.png'

# webserver setup
web_conf = WebserverConf(host="0.0.0.0", port=port)
web_server = Webserver(ip='localhost', conf=web_conf)

# robot_amount = 10

def calculate_amount(amount):
    robot_gets = int(amount) * 3
    # robot_has = robot_gets + robot_amount
    return [robot_gets, int(math.ceil(robot_gets * 2/3))]

# Callback function for Dialogflow response
def on_dialog(message):
    if message.response and message.response.recognition_result.is_final:
        print("Transcript:", message.response.recognition_result.transcript)

# Function to handle speech
def speak(text):
    print("Reply:", text)
    if reply.intent == "game_second_part":

         # Get the amount
        amount = int(reply.response.query_result.parameters["number"])
        print(amount)
        if amount > 10:
            nao.tts.request(NaoqiTextToSpeechRequest(f"You can't invest more than 10 euros. Please try again."))
        elif amount <= 0:
            nao.tts.request(NaoqiTextToSpeechRequest(f"You didn't invest anything. Thank you for playing the game! Please talk to my caretaker for filling out a survey"))
        else:
            calculated_amount = calculate_amount(amount)

            # Speak the response
            nao.tts.request(NaoqiTextToSpeechRequest(f"Thank you for investing {amount} euros. I now have {calculated_amount[0]} euros that I'll convert in energy."))
            time.sleep(1.0)

            if amount == 1:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T1))
            elif amount == 2:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T2))
            elif amount == 3:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T3))
            elif amount == 4:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T4))
            elif amount == 5:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T5))
            else:
                nao.tts.request(NaoqiTextToSpeechRequest(f"I was not able to calculate the amount. Please try again."))
            time.sleep(1.0)

            nao.tts.request(NaoqiTextToSpeechRequest(f"I decided that I will give you back two thirds of {calculated_amount[0]} which is {calculated_amount[1]}.")) 
            if amount == 1:
                nao.tablet_display_url.send_message(UrlMessage(web_url_low_battery))
            elif amount == 2:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T2_back))
            elif amount == 3:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T3_back))
            elif amount == 4:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T4_back))
            elif amount == 5:
                nao.tablet_display_url.send_message(UrlMessage(web_url_T5_back))
            else:
                nao.tts.request(NaoqiTextToSpeechRequest(f"Something went wrong. Please try again."))
            time.sleep(1.0)

            nao.tts.request(NaoqiTextToSpeechRequest(f"Thank you for playing the game! Please talk to my caretaker for filling out a survey"))        
            exit()

    # Speak the reply
    nao.tts.request(NaoqiTextToSpeechRequest(text))

# Function to handle motion
def move():
    if reply.intent == "game_second_part":
        amount = int(reply.response.query_result.parameters["number"])
        print(amount)
        if amount > 10:
            nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/No_1"))
        elif amount <= 0:
            nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Explain_1"))
        else:     
            nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Explain_8"))
            nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Give_3"))
            nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Explain_11"))

    
# Connect the output of NaoqiMicrophone as the input of DialogflowComponent
dialogflow.connect(nao.mic)

# Register a callback function for the recognition result
dialogflow.register_callback(on_dialog)

# Demo starts
nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Yes_1"))
nao.tts.request(NaoqiTextToSpeechRequest("The game is clear. How much money do you want to invest?"))
nao.tablet_display_url.send_message(UrlMessage(web_url_low_battery))
print(" -- Ready -- ")

# Random value for demo purposes
x = np.random.randint(10000)

# Loop for conversation turns
for i in range(25):
    print(" ----- Conversation turn", i)
    
    # Request intent from Dialogflow
    reply = dialogflow.request(GetIntentRequest(x))
    print(reply.intent)

    if reply.fulfillment_message:
        text = reply.fulfillment_message

        # Use threads to execute speech and motion concurrently
        speech_thread = threading.Thread(target=speak, args=(text,))
        motion_thread = threading.Thread(target=move)

        # Start both threads
        speech_thread.start()
        motion_thread.start()

        # Wait for both threads to finish
        speech_thread.join()
        motion_thread.join()
