import json
import numpy as np
import re
import random
import time

from sic_framework.core.utils import is_sic_instance
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, \
    GetIntentRequest, RecognitionResult, QueryResult, Dialogflow
from sic_framework.services.webserver.webserver_pepper_tablet import Webserver, HtmlMessage, WebserverConf, TranscriptMessage, ButtonClicked
from sic_framework.devices.common_naoqi.pepper_tablet import NaoqiTablet, UrlMessage
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from sic_framework.devices import Pepper

def on_dialog(message):
    """
    Callback function to handle dialogflow responses.
    """
    if is_sic_instance(message, RecognitionResult):
        # Assuming the HTML file is named 'image.html'
        html_file_path = "image1.html"
        with open(html_file_path) as file:
            html_content = file.read()

        # Send HTML content to the web server
        web_server.send_message(HtmlMessage(html_content))

        # Display the HTML on Pepper's tablet
        web_url = f'https://{machine_ip}:{port}/'
        pepper.tablet_display_url.send_message(UrlMessage(web_url))

        # Speak the recognized text
        pepper.tts.request(NaoqiTextToSpeechRequest(message.response.recognition_result.transcript))

port = 8080
machine_ip = '10.0.0.205'
robot_ip = '10.0.0.180'
# the HTML file to be rendered
html_file1 = "image1.html"
html_file2 = "image2.html" 
html_file3 = "image3.html"
web_url = f'https://{machine_ip}:{port}/'
# the random number that an user should guess
rand_int = random.randint(1, 10)

# Pepper device setup
pepper = Pepper(ip=robot_ip)

# webserver setup
web_conf = WebserverConf(host="0.0.0.0", port=port)
web_server = Webserver(ip='localhost', conf=web_conf)
# connect the output of webserver by registering it as a callback.
# the output is a flag to determine if the button has been clicked or not
#web_server.register_callback(on_button_click)

# dialogflow setup
keyfile_json = json.load(open("true-episode-411517-8a835be369c1.json"))
# local microphone
# sample_rate_hertz = 44100
# pepper's micriphone
sample_rate_hertz = 16000

conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=sample_rate_hertz)
dialogflow = Dialogflow(ip='localhost', conf=conf)
dialogflow.register_callback(on_dialog)
dialogflow.connect(pepper.mic)

# # send html to Webserver
# with open(html_file) as file:
#     data = file.read()
#     print("sending-------------")
#     web_server.send_message(HtmlMessage(data))
#     time.sleep(0.5)
#     # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
#     print("displaying html on Pepper display")
#     pepper.tablet_display_url.send_message(UrlMessage(web_url))

# Demo starts
pepper.tts.request(NaoqiTextToSpeechRequest("Hello, how are you?"))
print(" -- Ready -- ")
x = np.random.randint(10000)

# send html to Webserver
with open(html_file1) as file:
    data = file.read()
    print("sending-------------")
    web_server.send_message(HtmlMessage(data))
    time.sleep(0.5)
    # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
    print("displaying html on Pepper display")
    pepper.tablet_display_url.send_message(UrlMessage(web_url))

# for _ in range(3):
#     # Replace these image URLs with your actual image URLs
#     image_urls = ["image1.jpg", "image2.jpg", "image3.jpg"]
#     random_image_url = random.choice(image_urls)

#     # Display the image
#     with open(html_file) as file:
#         data = file.read()
#         print("sending-------------")
#         web_server.send_message(HtmlMessage(data))
#         time.sleep(0.5)
#         # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
#         print("displaying html on Pepper display")
#         pepper.tablet_display_url.send_message(UrlMessage(web_url))

#     time.sleep(5)  # Wait for 5 seconds between each image

for i in range(25):
    print(" ----- Conversation turn", i)
    reply = dialogflow.request(GetIntentRequest(x))

    print(reply.intent)

    if reply.fulfillment_message:
        text = reply.fulfillment_message
        print("Reply:", text)
        if reply.intent == "greetings - yes":
            with open(html_file2) as file:
                data = file.read()
                print("sending-------------")
                web_server.send_message(HtmlMessage(data))
                time.sleep(0.5)
                # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
                print("displaying html on Pepper display")
                pepper.tablet_display_url.send_message(UrlMessage(web_url))

        pepper.tts.request(NaoqiTextToSpeechRequest(text))