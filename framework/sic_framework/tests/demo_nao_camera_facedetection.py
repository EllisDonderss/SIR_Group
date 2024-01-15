# import queue

# import cv2

# from sic_framework.core import utils_cv2
# from sic_framework.core.message_python2 import BoundingBoxesMessage
# from sic_framework.core.message_python2 import CompressedImageMessage
# from sic_framework.devices.common_desktop.desktop_camera import DesktopCameraConf
# from sic_framework.devices.desktop import Desktop
# from sic_framework.services.face_detection.face_detection import FaceDetection
# import queue
# import cv2
# from sic_framework.core.message_python2 import CompressedImageMessage
# from sic_framework.devices import Nao

# """ 
# This demo recognizes faces from your webcam and displays the result on your laptop.

# You should have started the face detection service first with:
# [services/face_detection/] python face_detection.py
# """

# imgs_buffer = queue.Queue(maxsize=1)
# faces_buffer = queue.Queue(maxsize=1)


# def on_image(image_message: CompressedImageMessage):
#     imgs_buffer.put(image_message.image)


# def on_faces(message: BoundingBoxesMessage):
#     faces_buffer.put(message.bboxes)


# nao = Nao(ip="192.168.0.151")
# nao.top_camera.register_callback(on_image)


# # Connect to the services
# face_rec = FaceDetection()

# # Feed the camera images into the face recognition component
# face_rec.connect(nao.top_camera)

# # Send back the outputs to this program
# face_rec.register_callback(on_faces)

# while True:
#     img = imgs_buffer.get()
#     faces = faces_buffer.get()

#     for face in faces:
#         utils_cv2.draw_bbox_on_image(face, img)

#     cv2.imshow('', img)
#     cv2.waitKey(1)

import queue
import cv2

from sic_framework.core.message_python2 import CompressedImageMessage, BoundingBoxesMessage
from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_camera import NaoqiCameraConf
from sic_framework.services.face_detection.face_detection import FaceDetection
from sic_framework.core import utils_cv2

# Buffer for images and detected faces
imgs_buffer = queue.Queue(maxsize=1)
faces_buffer = queue.Queue(maxsize=1)

def on_image(image_message: CompressedImageMessage):
    imgs_buffer.put(image_message.image)

def on_faces(message: BoundingBoxesMessage):
    faces_buffer.put(message.bboxes)

# Create NAO camera configuration
conf = NaoqiCameraConf()  # Adjust as needed

# Initialize NAO with camera configuration
nao = Nao(ip="192.168.0.151", top_camera_conf=conf)

# Initialize face detection service
face_rec = FaceDetection()

# Connect the NAO camera to the face recognition component
face_rec.connect(nao.top_camera)

# Register callbacks
nao.top_camera.register_callback(on_image)
face_rec.register_callback(on_faces)

while True:
    img = imgs_buffer.get()
    faces = faces_buffer.get()

    for face in faces:
        utils_cv2.draw_bbox_on_image(face, img)

    # Display the image. Note: cv2 uses BGR format
    cv2.imshow('', img[..., ::-1])
    cv2.waitKey(1)