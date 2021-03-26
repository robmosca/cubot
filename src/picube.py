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

    def capture(self):
        img = np.empty((CubotCam.IMG_HEIGHT * CubotCam.IMG_WIDTH * 3,), dtype=np.uint8)
        self.cam.capture(img, "bgr")
        self.orig_face = img.reshape((CubotCam.IMG_HEIGHT, CubotCam.IMG_WIDTH, 3))

        pts1 = np.float32([[140, 180], [465, 180], [-30, 465], [620, 465]])
        pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        self.square_face = cv2.warpPerspective(self.orig_face, M, (300, 300))

    def save_capture(self, img_name):
        cv2.imwrite("images/%s-orig.png" % img_name, self.orig_face)
        cv2.imwrite("images/%s-square.png" % img_name, self.square_face)


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

        print("⏳ Waiting for command...")
        while True:
            try:
                input_data = self.port.readline()
                decoded_data = str(input_data.decode("utf-8"))
                lines = decoded_data.split("\r")
                for line in lines:
                    command, *args = line.split()
                    print("Command:", command, *args)
                    if command in PiCube.COMMANDS:
                        return (command, args)
            except Exception as e:
                print("Error while receiving data from Cubot, disconnecting...")
                self.disconnect()
                raise e

    def send_reponse(self, response):
        self.port.write(bytes(response + "\n\r", "utf-8"))
        print("Response sent (%s)" % response)

    def run(self):
        while True:
            command, args = self.wait_for_command()
            print("⚙️ Command received: '%s'" % command)
            if command == "EXIT":
                print("Exiting...")
                return
            elif command == "IMAGE":
                img_name = args[0]
                print("Saving image %s..." % img_name)
                self.cubot_cam.capture()
                self.cubot_cam.save_capture(img_name)
                time.sleep(0.2)
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
