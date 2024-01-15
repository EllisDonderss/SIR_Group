import time

from nao_small_talk_dominant import dialogflow_start
from multiprocessing import Process
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest, NaoqiBreathingRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest, NaoLEDRequest
from sic_framework.devices.common_naoqi.naoqi_autonomous import (
    NaoWakeUpRequest,
    NaoRestRequest,
    NaoBasicAwarenessRequest
)
from sic_framework.devices.nao import Nao

from argparse import ArgumentParser

def main(placeholder, nao):
    try:
        # Wake up Nao
        print("Waking up Nao...")
        nao.autonomous.request(NaoWakeUpRequest())
        time.sleep(1)

        # Enable Basic Awareness for face tracking
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

        # Stop all movement and breathing by pressing Enter
        input("Press Enter to stop Nao and exit...")

    finally:
        # Turn off awareness and go to rest position
        print("Disabling Basic Awareness and resting Nao...")
        nao.autonomous.request(NaoBasicAwarenessRequest(value=False))
        nao.autonomous.request(NaoRestRequest())
        print("Nao is now resting.")


def perform_actions(nao):
    ''' Exterior look/behaviour of the robot, including breathing, movement (gestures) and the lighting colours. '''
    
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
    # Akimbo position --> Hands on hips
    recording = NaoqiMotionRecording.load("gestures/dominant/framework/dominant_akimbo_updated.motion")
    nao.motion_record.request(PlayRecording(recording))
    # game_start(mode_dict["dominant"])
    time.sleep(1)

    # Go to neutral position
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))

    # Stop Breathing Behavior
    print("Stopping Breathing Behavior...")
    nao.motion.request(NaoqiBreathingRequest("Body", False))

if __name__ == '__main__':
    main()
