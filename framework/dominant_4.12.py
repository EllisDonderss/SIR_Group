import time
import json

from nao_smallTalk import dialogflow_start
from multiprocessing import Process
from argparse import ArgumentParser
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest, NaoqiBreathingRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest, NaoLEDRequest
from sic_framework.devices.common_naoqi.naoqi_autonomous import (
    NaoWakeUpRequest,
    NaoRestRequest,
    NaoBasicAwarenessRequest
)


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

# connect to the robot
# get ip key from json ip_key.json file
with open('ip_key.json') as f:
    data = json.load(f)
ip_key = data['ip_key']

nao = Nao(ip_key)

# paralelizing functions
def runInParallel(functions):
    proc = []
    for nao_function in functions:
        p = Process(target=nao_function)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def main():
    try:
        # Wake up Nao
        print("Waking up Nao...")
        nao.autonomous.request(NaoWakeUpRequest())
        time.sleep(1)

        # Enable Basic Awareness for person tracking
        print("Enabling Basic Awareness for person tracking...")
        basic_awareness_request = NaoBasicAwarenessRequest(
            value=True, 
            engagement_mode="FullyEngaged", 
            tracking_mode="Head"
        )
        nao.autonomous.request(basic_awareness_request)
        time.sleep(1)

        # Perform predefined gestures and actions
        runInParallel([dialogflow_start, perform_actions])

        # Wait for user input to stop
        input("Press Enter to stop Nao and exit...")

    finally:
        # Turn off awareness and go to rest position
        print("Disabling Basic Awareness and resting Nao...")
        nao.autonomous.request(NaoBasicAwarenessRequest(value=False))
        nao.autonomous.request(NaoRestRequest())
        print("Nao is now resting.")

def perform_actions():
    # Starting stance
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))
    time.sleep(1)

    # Start Breathing Behavior
    print("Starting Breathing Behavior...")
    nao.motion.request(NaoqiBreathingRequest("Body", True))
    time.sleep(1)

    # Yellow lights
    nao.leds.request(NaoFadeRGBRequest("AllLeds", 1, 0.8, 0.1, 0))
    # Turn off lights on top of head and ears
    nao.leds.request(NaoLEDRequest("BrainLeds", False))
    nao.leds.request(NaoLEDRequest("EarLeds", False))
    time.sleep(1)

    # Dominant gestures
    # Akimbo position
    recording = NaoqiMotionRecording.load("gestures/dominant/dominant_akimbo.motion")
    nao.motion_record.request(PlayRecording(recording))
    time.sleep(1)

    # Go to neutral position
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))

    # Stop Breathing Behavior
    print("Stopping Breathing Behavior...")
    nao.motion.request(NaoqiBreathingRequest("Body", False))

if __name__ == '__main__':
    main()
