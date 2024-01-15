import time
import json
import threading

from nao_small_talk_submisive import dialogflow_start
import final_submissive
from sic_framework.devices.common_naoqi.naoqi_autonomous import (
    NaoWakeUpRequest,
    NaoRestRequest,
    NaoBasicAwarenessRequest
)
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.nao import Nao
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, Dialogflow, GetIntentRequest, QueryResult, RecognitionResult)


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

# Connect to the robot using the ip from ip_key.json
with open('ip_key.json') as f:
    data = json.load(f)
ip_key = data['ip_key']

nao = Nao(ip_key)

def play_animation(nao, animation_path):
    recording = NaoqiMotionRecording.load(animation_path)
    nao.motion_record.request(PlayRecording(recording))

def play_combined_motion(nao):
    ''' Play simultaneously the movement of the Nao robot and the Dialogflow using threading. '''
    # Create threads for each animation
    motion_thread = threading.Thread(target=final_submissive.main, args=(None, nao))
    # For some reason passing the function with just nao as an argument does not work, since it expects an array.
    # I gave it None which made it pass and work
    speech_thread = threading.Thread(target=dialogflow_start, args=(None, nao))

    # Start threads
    speech_thread.start()  
    motion_thread.start()

    # Wait for both threads to complete, if one isn't done, the other will repeat until both are finished.
    speech_thread.join()
    motion_thread.join()


def main():
    try:
        # Wake up Nao
        nao.autonomous.request(NaoWakeUpRequest())
        time.sleep(1)

        # Starting stance and LED color
        nao.motion.request(NaoPostureRequest("Crouch", 0.5))
        nao.leds.request(NaoFadeRGBRequest("AllLeds", 1, 0.1, 1, 0))

        # Perform predefined gestures and actions
        play_combined_motion(nao)
        print("Done with submissive position")

    finally:
        # Go to rest position
        nao.motion.request(NaoPostureRequest("Crouch", 0.5))
        nao.autonomous.request(NaoRestRequest())

if __name__ == '__main__':
    main()