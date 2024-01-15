import time

from sic_framework.devices.common_naoqi.naoqi_motion import NaoqiIdlePostureRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import StartRecording, StopRecording, PlayRecording, NaoqiMotionRecorderConf, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from sic_framework.devices.nao import Nao
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_motion import NaoPostureRequest

conf = NaoqiMotionRecorderConf(use_sensors=True, use_interpolation=True, samples_per_second=60)

nao = Nao("192.168.0.138", motion_record_conf=conf)




print("Set robot to start position")

chain = ["Head", "RArm", "LArm"]

# Disable "alive" activity for the whole body and set stiffness of the arm to zero
nao.motion.request(NaoqiIdlePostureRequest("Body", False))
reply = nao.motion.request(NaoPostureRequest("Stand", .5))


recording = NaoqiMotionRecording.load("akimbo.motion")
# nao.motion_record.request(StopRecording())
# recording.save("submissive.motion")

print("Done")

time.sleep(2)

print("Replaying action")
# recording = NaoqiMotionRecording.load("wave.motion")

nao.stiffness.request(Stiffness(.95, chain))

nao.motion_record.request(PlayRecording(recording))

nao.stiffness.request(Stiffness(0, chain))


print("end")

nao.motion.request(NaoPostureRequest("Crouch", .5))




