import json
import numpy as np
import re
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
from sic_framework.devices.nao import NaoqiTextToSpeechRequest, NaoqiMoveRequest, NaoqiAnimationRequest
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, GetIntentRequest, Dialogflow, RecognitionResult, QueryResult
from sic_framework.core import *


# Connect to the robot
nao = Pepper(ip='10.0.0.164')

# Load the key json file
keyfile_json = json.load(open("true-episode-411517-8a835be369c1.json"))

# Set up the Dialogflow config
conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

# Initiate Dialogflow object
dialogflow = Dialogflow(ip='localhost', conf=conf)

port = 8080
web_url_T2 = f'https://media.githubusercontent.com/media/EllisDonderss/SIR_Group/new/framework/UI%20pepper/T2.png'
web_url_T1 = f'https://media.githubusercontent.com/media/EllisDonderss/SIR_Group/new/framework/UI%20pepper/Begin_State.png'

# webserver setup
web_conf = WebserverConf(host="0.0.0.0", port=port)
web_server = Webserver(ip='localhost', conf=web_conf)

# Callback function for Dialogflow response
def on_dialog(message):
    if message.response and message.response.recognition_result.is_final:
        print("Transcript:", message.response.recognition_result.transcript)

# Function to handle speech
def speak(text):
    print("Reply:", text)
    if reply.intent == "greetings - custom":
        nao.tts.request(NaoqiTextToSpeechRequest(text))
        time.sleep(1.0)
        nao.tablet_display_url.send_message(UrlMessage(web_url_T1))
        nao.tts.request(NaoqiTextToSpeechRequest(f"Oh no! I see that my battery is running low. That is unfortunate."))
        # stop the conversation
        exit()
    # Speak the reply
    nao.tts.request(NaoqiTextToSpeechRequest(text))

# Function to handle motion
def move():
    # Move robot arms while speaking
    nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Explain_1"))

# Connect the output of NaoqiMicrophone as the input of DialogflowComponent
dialogflow.connect(nao.mic)

# Register a callback function for the recognition result
dialogflow.register_callback(on_dialog)

# Demo starts
a = nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Hey_3"))
b = nao.tablet_display_url.send_message(UrlMessage(web_url_T2))
c = nao.tts.request(NaoqiTextToSpeechRequest("Hello, how are you?"))

# Use threads to execute speech and motion concurrently
first = threading.Thread(target=b)
second = threading.Thread(target=a)
third = threading.Thread(target=c)

# Start both threads
first.start()
second.start()
third.start()

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

