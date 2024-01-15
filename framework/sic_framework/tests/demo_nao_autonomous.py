import time

from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_autonomous import (NaoWakeUpRequest, NaoBlinkingRequest,
                                                                 NaoSpeakingMovementRequest, NaoRestRequest,
                                                                 NaoBasicAwarenessRequest, NaoListeningMovementRequest,
                                                                 NaoBackgroundMovingRequest)

nao = Nao(ip="192.168.0.151")

print("Requesting NaoRestRequest")
reply = nao.autonomous.request(NaoRestRequest())
time.sleep(1)

# print("Requesting wakeUp")
# reply = nao.autonomous.request(NaoWakeUpRequest())
# time.sleep(1)

# print("Requesting Autonomous blinking on")
# reply = nao.autonomous.request(NaoBlinkingRequest(True))
# time.sleep(1)

# print("Requesting NaoSpeakingMovementRequest")
# reply = nao.autonomous.request(NaoSpeakingMovementRequest(True))
# time.sleep(1)

# print("Requesting NaoBasicAwarenessRequest")
# reply = nao.autonomous.request(NaoBasicAwarenessRequest(False, stimulus_detection = [("Sound", False,), ("People", False)]))
# time.sleep(1)

# print("Requesting NaoListeningMovementRequest")
# reply = nao.autonomous.request(NaoListeningMovementRequest(False))
# time.sleep(1)
# #
# print("Requesting NaoBackgroundMovingRequest")
# reply = nao.autonomous.request(NaoBackgroundMovingRequest(False))
# time.sleep(1)
