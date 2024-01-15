import time
import json

from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest, NaoqiBreathingRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest, NaoLEDRequest
from sic_framework.devices.common_naoqi.naoqi_autonomous import NaoWakeUpRequest, NaoRestRequest

def main(plaeholder, nao): 
    # Call actions from function
    perform_actions(nao)
    

def perform_actions(nao):
    ''' Exterior behaviour of the robot, stance and colour of LEDS lights. '''
    # Starting stance
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))
    time.sleep(1)

    # Pink lights
    nao.leds.request(NaoFadeRGBRequest("AllLeds", 1, 0.1, 1, 0))
    # Turn off lights on top of head and ears
    nao.leds.request(NaoLEDRequest("BrainLeds", False))
    nao.leds.request(NaoLEDRequest("EarLeds", False))
    time.sleep(1)

    # Go to neutral position if for some reason it isn't already.
    nao.motion.request(NaoPostureRequest("Crouch", 0.5))

    # Submissive gestures from [play_combined_motion] function.
    play_combined_motion(nao)


def play_combined_motion(nao):
    ''' Movement of the robot, the robot will be seated in the 'crouch' position with its hands crossed over its
    chest. '''
    # Load and play motions concurrently
    submissive_recording = NaoqiMotionRecording.load("gestures/submissive/submissive_cross.motion")
    # Play recording
    nao.motion_record.request(PlayRecording(submissive_recording))
    time.sleep(1)


if __name__ == '__main__':
    main()
