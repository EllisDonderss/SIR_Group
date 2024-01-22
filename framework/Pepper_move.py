import json
import numpy as np
import time
import threading

from sic_framework.devices import Pepper
from sic_framework.devices.nao import NaoqiTextToSpeechRequest, NaoqiMoveRequest, NaoqiAnimationRequest
from sic_framework.services.dialogflow.dialogflow import DialogflowConf, GetIntentRequest, Dialogflow, RecognitionResult, QueryResult
from sic_framework.core import *


# Callback function for Dialogflow response
def on_dialog(message):
    if message.response and message.response.recognition_result.is_final:
        print("Transcript:", message.response.recognition_result.transcript)

# Function to handle speech
def speak(text):
    print("Reply:", text)
    # Speak the reply
    nao.tts.request(NaoqiTextToSpeechRequest(text))

# Function to handle motion
def move():
    # Move robot arms while speaking
    nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Explain_1"))

# Connect to the robot
nao = Pepper(ip='10.0.0.164')

# Load the key json file
keyfile_json = json.load(open("true-episode-411517-8a835be369c1.json"))

# Set up the Dialogflow config
conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=16000)

# Initiate Dialogflow object
dialogflow = Dialogflow(ip='localhost', conf=conf)

# Connect the output of NaoqiMicrophone as the input of DialogflowComponent
dialogflow.connect(nao.mic)

# Register a callback function for the recognition result
dialogflow.register_callback(on_dialog)

# Demo starts
a = nao.motion.request(NaoqiAnimationRequest("animations/Stand/Gestures/Hey_3"))
b = nao.tts.request(NaoqiTextToSpeechRequest("Hello, how are you?"))
# Use threads to execute speech and motion concurrently
first = threading.Thread(target=b)
second = threading.Thread(target=a)

# Start both threads
first.start()
second.start()

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


###################################################################
        

# def on_dialog(message):
#     """
#     Callback function to handle dialogflow responses.
#     """
#     if is_sic_instance(message, RecognitionResult):
#         # Assuming the HTML file is named 'image.html'
#         html_file_path = "image1.html"
#         with open(html_file_path) as file:
#             html_content = file.read()

#         # Send HTML content to the web server
#         web_server.send_message(HtmlMessage(html_content))

#         # Display the HTML on Pepper's tablet
#         web_url = f'https://{machine_ip}:{port}/'
#         pepper.tablet_display_url.send_message(UrlMessage(web_url))

#         # Speak the recognized text
#         pepper.tts.request(NaoqiTextToSpeechRequest(message.response.recognition_result.transcript))

# port = 8080
# machine_ip = '10.0.0.205'
# robot_ip = '10.0.0.180'
# # the HTML file to be rendered
# html_file1 = "image1.html"
# html_file2 = "image2.html" 
# html_file3 = "image3.html"
# web_url = f'https://{machine_ip}:{port}/'
# # the random number that an user should guess
# rand_int = random.randint(1, 10)

# # Pepper device setup
# pepper = Pepper(ip=robot_ip)

# # webserver setup
# web_conf = WebserverConf(host="0.0.0.0", port=port)
# web_server = Webserver(ip='localhost', conf=web_conf)
# # connect the output of webserver by registering it as a callback.
# # the output is a flag to determine if the button has been clicked or not
# #web_server.register_callback(on_button_click)

# # dialogflow setup
# keyfile_json = json.load(open("true-episode-411517-8a835be369c1.json"))
# # local microphone
# # sample_rate_hertz = 44100
# # pepper's micriphone
# sample_rate_hertz = 16000

# conf = DialogflowConf(keyfile_json=keyfile_json, sample_rate_hertz=sample_rate_hertz)
# dialogflow = Dialogflow(ip='localhost', conf=conf)
# dialogflow.register_callback(on_dialog)
# dialogflow.connect(pepper.mic)

# # # send html to Webserver
# # with open(html_file) as file:
# #     data = file.read()
# #     print("sending-------------")
# #     web_server.send_message(HtmlMessage(data))
# #     time.sleep(0.5)
# #     # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
# #     print("displaying html on Pepper display")
# #     pepper.tablet_display_url.send_message(UrlMessage(web_url))

# # Demo starts
# pepper.tts.request(NaoqiTextToSpeechRequest("Hello, how are you?"))
# print(" -- Ready -- ")
# x = np.random.randint(10000)

# # send html to Webserver
# with open(html_file1) as file:
#     data = file.read()
#     print("sending-------------")
#     web_server.send_message(HtmlMessage(data))
#     time.sleep(0.5)
#     # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
#     print("displaying html on Pepper display")
#     pepper.tablet_display_url.send_message(UrlMessage(web_url))

# # for _ in range(3):
# #     # Replace these image URLs with your actual image URLs
# #     image_urls = ["image1.jpg", "image2.jpg", "image3.jpg"]
# #     random_image_url = random.choice(image_urls)

# #     # Display the image
# #     with open(html_file) as file:
# #         data = file.read()
# #         print("sending-------------")
# #         web_server.send_message(HtmlMessage(data))
# #         time.sleep(0.5)
# #         # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
# #         print("displaying html on Pepper display")
# #         pepper.tablet_display_url.send_message(UrlMessage(web_url))

# #     time.sleep(5)  # Wait for 5 seconds between each image

# for i in range(25):
#     print(" ----- Conversation turn", i)
#     reply = dialogflow.request(GetIntentRequest(x))

#     print(reply.intent)

#     if reply.fulfillment_message:
#         text = reply.fulfillment_message
#         print("Reply:", text)
#         if reply.intent == "greetings - yes":
#             with open(html_file2) as file:
#                 data = file.read()
#                 print("sending-------------")
#                 web_server.send_message(HtmlMessage(data))
#                 time.sleep(0.5)
#                 # once an HTML content has been sent to the web server, a url is sent to Pepper to be displayed
#                 print("displaying html on Pepper display")
#                 pepper.tablet_display_url.send_message(UrlMessage(web_url))

#         pepper.tts.request(NaoqiTextToSpeechRequest(text))