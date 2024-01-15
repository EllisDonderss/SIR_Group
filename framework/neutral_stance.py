import time
import json
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest
from sic_framework.devices.common_naoqi.naoqi_leds import NaoFadeRGBRequest, NaoLEDRequest
from sic_framework.devices.common_naoqi.naoqi_autonomous import NaoWakeUpRequest, NaoRestRequest

# Load IP address from JSON file
with open('ip_key.json') as f:
    data = json.load(f)
ip_key = data['ip_key']

# Initialize Nao robot
nao = Nao(ip_key)

def main():
    ''' This code will result in the robot standing straight up, with white lights coming from the eyes, all other
    lights are off, this represents a neutral stance.
    This code is not used in the experimental setup. '''
    try:
        # Wake up Nao
        nao.autonomous.request(NaoWakeUpRequest())

        # Starting stance and LED color
        nao.leds.request(NaoFadeRGBRequest("AllLeds", 1, 1, 1, 1))
        # Turn off lights on top of head and ears
        nao.leds.request(NaoLEDRequest("BrainLeds", False))
        nao.leds.request(NaoLEDRequest("EarLeds", False))

        nao.motion.request(NaoPostureRequest("Stand", 0.5))
        time.sleep(15) # Stand for 15 seconds
        
        print("Done with Neutral position")

    finally:
        # Go to rest position
        nao.autonomous.request(NaoRestRequest())


if __name__ == '__main__':
    main()
