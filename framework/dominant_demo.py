import time
from sic_framework.devices import Nao
from sic_framework.devices.nao import NaoqiTextToSpeechRequest
from sic_framework.services.dialogflow.dialogflow import (DialogflowConf, GetIntentRequest, RecognitionResult,
                                                          QueryResult, Dialogflow)

from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest
from sic_framework.devices.common_naoqi.naoqi_autonomous import (
    NaoWakeUpRequest,
    NaoRestRequest,
    NaoBasicAwarenessRequest
)
import json


def main():
    # get ip key from json ip_key.json file
    with open('ip_key.json') as f:
        data = json.load(f)

    ip_key = data['ip_key']
    print(ip_key)
    nao = Nao(ip=ip_key)

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
        perform_actions(nao)

        # Wait for user input to stop
        input("Press Enter to stop Nao and exit...")

    finally:
        # Turn off awareness and go to rest position
        print("Disabling Basic Awareness and resting Nao...")
        nao.autonomous.request(NaoBasicAwarenessRequest(value=False))
        nao.autonomous.request(NaoRestRequest())
        print("Nao is now resting.")

def perform_actions(nao):
    # Starting stance
    nao.motion.request(NaoPostureRequest("Stand", 0.5))
    time.sleep(1)

    # Red lights
    nao.leds.request(NaoFadeRGBRequest("AllLeds", 1, 0, 0, 0))
    time.sleep(1)

    # Dominant gestures
    # Akimbo position
    recording = NaoqiMotionRecording.load("gestures/dominant/akimbo.motion")
    nao.motion_record.request(PlayRecording(recording))
    time.sleep(1)

    # Dominant head tilt
    recording = NaoqiMotionRecording.load("gestures/dominant/dominant_head_tilt.motion")
    nao.motion_record.request(PlayRecording(recording))
    time.sleep(1)

    # Go to neutral position
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))

if __name__ == "__main__":
    main()



