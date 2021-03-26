import cv2
import numpy as np
import picamera
import serial
import time


class CubotCam:
    IMG_WIDTH = 640
    IMG_HEIGHT = 480

    @staticmethod
    def _init_pi_cam():
        camera = picamera.PiCamera()
        camera.resolution = (CubotCam.IMG_WIDTH, CubotCam.IMG_HEIGHT)
        camera.framerate = 24
        camera.start_preview(
            fullscreen=False, window=(1320, 10, CubotCam.IMG_WIDTH, CubotCam.IMG_HEIGHT)
        )
        time.sleep(2)
        return camera

    def __init__(self):
        self.cam = CubotCam._init_pi_cam()
        self.orig_face = None
        self.square_face = None
        self.norm_face = None

    def capture(self):
        img = np.empty((CubotCam.IMG_HEIGHT * CubotCam.IMG_WIDTH * 3,), dtype=np.uint8)
        self.cam.capture(img, "bgr")
        self.orig_face = img.reshape((CubotCam.IMG_HEIGHT, CubotCam.IMG_WIDTH, 3))

        pts1 = np.float32([[155, 185], [480, 185], [-40, 480], [610, 480]])
        pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        self.square_face = cv2.warpPerspective(self.orig_face, M, (300, 300))


class PiCube:
    LEGO_HUB_DEVICE = "/dev/ttyACM0"
    COMMANDS = {"IMAGE", "EXIT"}

    def __init__(self):
        self.cubot_cam = CubotCam()
        self.port = None

    def connect(self):
        print("🔌 Connecting to Cubot...")
        try:
            self.port = serial.Serial(PiCube.LEGO_HUB_DEVICE)
            print("🎉 Cubot connected!!")
            return True
        except Exception:
            print(
                "❗Cannot connect to Cubot. Make sure the Hub is connected and powered..."
            )
            self.port = None
            return False

    def disconnect(self):
        self.port.close()
        self.port = None
        print("🚫 Cubot disconnected!!")

    def wait_for_command(self):
        if self.port is None:
            raise Exception("Cubot is not connected")

        while True:
            try:
                input_data = self.port.readline()
                decoded_data = str(input_data.decode("utf-8"))
                command, *arguments = decoded_data.split()
                if command in PiCube.COMMANDS:
                    return (command, *arguments)
            except Exception:
                print("Error while receiving data from Cubot, disconnecting...")
                self.disconnect()

    def send_reponse(self, response):
        self.port.write(response + "\n")

    def run(self):
        while True:
            command, args = self.wait_for_command()
            print(command)
            if command == "EXIT":
                print("Exiting...")
                return
            elif command == "IMAGE":
                img_name = args[0] + ".png"
                print("Saving image %s..." % img_name)
                self.cubot_cam.capture(img_name)
                self.send_reponse("OK")


pi_cube = PiCube()
if pi_cube.connect():
    pi_cube.run()
    pi_cube.disconnect()


# c = CubotCam()
# c.capture()
# cv2.namedWindow("image")
# for img in [c.orig_face, c.square_face, c.norm_face]:
#     cv2.imshow("image", img)
#     cv2.waitKey(0)
