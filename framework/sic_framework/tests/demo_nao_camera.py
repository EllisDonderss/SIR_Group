import queue
import cv2
from sic_framework.core.message_python2 import CompressedImageMessage
from sic_framework.devices import Nao

imgs = queue.Queue()


def on_image(image_message: CompressedImageMessage):
    # we could use cv2.imshow here, but that does not work on Mac OSX
    imgs.put(image_message.image)


nao = Nao(ip="192.168.0.151")
nao.top_camera.register_callback(on_image)

while True:
    img = imgs.get()
    cv2.imshow('', img[..., ::-1])  # cv2 is BGR instead of RGB
    cv2.waitKey(1)
