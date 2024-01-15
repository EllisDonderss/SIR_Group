import time

from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest, NaoqiBreathingRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest


def perform_actions(nao):
    # Starting stance
    nao.motion.request(NaoPostureRequest("Stand", 0.5))
    time.sleep(1)

    # Start Breathing Behavior
    print("Starting Breathing Behavior...")
    nao.motion.request(NaoqiBreathingRequest("Body", True))
    time.sleep(1)

    # Red lights
    nao.leds.request(NaoFadeRGBRequest("AllLeds", 1, 0, 0, 0))
    time.sleep(1)

    # Dominant gestures
    # Akimbo position
    recording = NaoqiMotionRecording.load("gestures/dominant/akimbo.motion")
    nao.motion_record.request(PlayRecording(recording))
    # game_start(mode_dict["dominant"])
    time.sleep(1)

    # Go to neutral position
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))

    # Stop Breathing Behavior
    print("Stopping Breathing Behavior...")
    nao.motion.request(NaoqiBreathingRequest("Body", False))
