from io import BytesIO
import asyncio
import logging
import subprocess

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

class LogcatNotRunningError(Exception):
    pass

class PokemonGo(object):
    def __init__(self):
        self.device_id = None

    async def set_device(self, device_id=None):
        self.device_id = device_id

    async def get_device(self):
        if self.device_id:
            return self.device_id
        devices = await self.get_devices()
        if devices == []:
            raise PhoneNotConnectedError
        self.device_id = devices[0]
        return self.device_id

    async def run(self, args):
        logger.debug("Running %s", args)
        p = subprocess.Popen([str(arg) for arg in args], stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        logger.debug("Return code %d", p.returncode)
        return (p.returncode, stdout, stderr)

    async def get_devices(self):
        code, stdout, stderr = await self.run(["adb", "devices"])
        devices = []
        for line in stdout.decode('utf-8').splitlines()[1:-1]:
            device_id, name = line.split('\t')
            devices.append(device_id)
        return devices

    async def start_logcat(self):
        return_code, stdout, stderr = await self.run(["adb", "-s", await self.get_device(), "shell", "pidof", "-s", "tesmath.calcy"])
        logger.debug("Running pidof calcy got code %d: %s", stdout)
        pid = stdout.decode('utf-8').strip()
        cmd = ["adb", "-s", await self.get_device(), "logcat", "--pid={}".format(pid)]
        logger.debug("Starting logcat %s", cmd)
        self.logcat_task = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Seek to the end of the file
        while True:
            try:
                task = await asyncio.wait_for(self.read_logcat(), 0.1)
            except asyncio.TimeoutError:
                break

    async def read_logcat(self):
        if self.logcat_task.returncode != None:
            logger.error("Logcat process is not running")
            logger.error("stdout %s", await self.logcat_task.stdout.read())
            logger.error("stderr %s", await self.logcat_task.stderr.read())
            raise LogcatNotRunningError()
            
        line = await self.logcat_task.stdout.readline()
        logger.debug("Received logcat line: %s", line)
        return line

    async def send_intent(self, intent, package):
        await self.run(["adb", "-s", await self.get_device(), "shell", "am broadcast -a {} -n {}".format(intent, package)])

    async def tap(self, x, y):
        await self.run(["adb", "-s", await self.get_device(), "shell", "input", "tap", x, y])

    async def key(self, key):
        await self.run(["adb", "-s", self.device_id, "shell", "input", "keyevent", key])
