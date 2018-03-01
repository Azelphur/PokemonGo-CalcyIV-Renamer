import time
import argparse
import subprocess
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger('PokemonGo')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class CalcyIVError(Exception):
    pass

class RedBarError(Exception):
    pass

class PhoneNotConnectedError(Exception):
    pass

class PokemonGo(object):
    def __init__(self, device_id):
        devices = self.get_devices()
        if devices == [] or (device_id is not None and device_id not in devices):
            raise PhoneNotConnectedError
        if device_id is None:
            self.device_id = devices[0]
        else:
            self.device_id = device_id
        self.resolution = None

    def run(self, args):
        logger.debug("Running %s", args)
        p = subprocess.Popen([str(arg) for arg in args], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        logger.debug("Return code %d", p.returncode)
        return (p.returncode, stdout, stderr)

    def screencap(self):
        return_code, stdout, stderr = self.run(["adb", "-s", self.device_id, "shell", "screencap", "-p"])
        image = Image.open(BytesIO(stdout))
        return image

    def determine_resolution(self):
        image = self.screencap()
        logger.info("Determined device resolution as %s", image.size)
        return image.size

    def get_resolution(self):
        if self.resolution is None:
            self.resolution = self.determine_resolution()
        return self.resolution

    def get_x(self, percent):
        width, height = self.get_resolution()
        return int((width / 100) * percent)

    def get_y(self, percent):
        width, height = self.get_resolution()
        return int((height / 100) * percent)

    def tap(self, x, y, sleep):
        self.run(["adb", "-s", self.device_id, "shell", "input", "tap", self.get_x(x), self.get_y(y)])
        time.sleep(sleep)

    def key(self, key, sleep):
        self.run(["adb", "-s", self.device_id, "shell", "input", "keyevent", key])
        time.sleep(sleep)

    def swipe(self, x1, y1, x2, y2, sleep, duration=None):
        width, height = self.get_resolution()
        args = [
            "adb",
            "-s",
            self.device_id,
            "shell",
            "input",
            "swipe",
            self.get_x(x1),
            self.get_y(y1),
            self.get_x(x2),
            self.get_y(y2)
        ]
        if duration:
            args.append(duration)
        self.run(args)
        time.sleep(sleep)

    def check_pixel(self, rgb_image, x, y, rgb):
        img_rgb = rgb_image.getpixel((self.get_x(x), self.get_y(y)))
        logger.debug("Checking pixel. %dx%d image is %s, want %s. Returning %s", self.get_x(x), self.get_y(y), img_rgb, rgb, img_rgb == rgb)
        return img_rgb == rgb
        
    def check_calcy_iv(self):
        image = self.screencap()
        rgb_image = image.convert('RGB')
        if self.check_pixel(rgb_image, 50, 89.28, (0x44, 0x69, 0x6C)) is False: # Calcy IV Failed?
            if self.check_pixel(rgb_image, 4.62, 6.77, (0xF0, 0x4B, 0x5F)) is True:
                raise RedBarError
            else:
                raise CalcyIVError

    def get_devices(self):
        code, stdout, stderr = self.run(["adb", "devices"])
        devices = []
        for line in stdout.decode('utf-8').splitlines()[1:-1]:
            device_id, name = line.split('\t')
            devices.append(device_id)
        return devices
