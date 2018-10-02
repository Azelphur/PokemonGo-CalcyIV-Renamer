from pokemonlib import PokemonGo
import yaml
import asyncio
import re
import argparse
from sys import platform

RE_CALCY_IV = re.compile(r"^MainService: Received values: Id: \d+ \((?P<name>.+)\), Nr: (?P<id>\d+), CP: (?P<cp>\d+), Max HP: (?P<max_hp>\d+), Dust cost: (?P<dust_cost>\d+), Level: (?P<level>[0-9\.]+), FastMove (?P<fast_move>.+), SpecialMove (?P<special_move>.+), Gender (?P<gender>\d)$")
RE_RED_BAR = re.compile(r"^av      : Screenshot #\d has red error box at the top of the screen$")
RE_SUCCESS = re.compile(r".+\s+: calculateScanOutputData finished after \d+ms$")
RE_SCAN_INVALID = re.compile(r".+\s+: Scan invalid$")


class CalcyIVError(Exception):
    pass


class RedBarError(Exception):
    pass


class Main:
    def __init__(self, args):
        with open(args.config, "r") as f:
            self.config = yaml.load(f)
        self.args = args

    async def tap(self, location):
        await self.p.tap(*self.config['locations'][location])
        if location in self.config['waits']:
            await asyncio.sleep(self.config['waits'][location])

    async def swipe(self, location, duration):
        await self.p.swipe(
            self.config['locations'][location][0],
            self.config['locations'][location][1],
            self.config['locations'][location][0],
            self.config['locations'][location][1],
            duration
        )
        if location in self.config['waits']:
            await asyncio.sleep(self.config['waits'][location])   

    async def start(self):
        self.p = PokemonGo()
        await self.p.start_logcat()
        num_errors = 0
        while True:
            try:
                values = await self.check_pokemon()
                await self.p.seek_to_end() # just in case any additional lines are present
                num_errors = 0
            except RedBarError:
                continue
            except CalcyIVError:
                num_errors += 1
                if num_errors > args.max_retries:
                    await self.tap('next')
                    num_errors = 0
                continue

            await self.tap('dismiss_calcy')
            await self.tap('rename')
            if args.touch_paste:
                await self.swipe('edit_box', 600)
                await self.tap('paste')

            else:
                await self.p.key(279) # Paste into rename
            await self.tap('keyboard_ok')
            await self.tap('rename_ok')
            await self.tap('next')

    async def check_pokemon(self):
        await self.p.send_intent("tesmath.calcy.ACTION_ANALYZE_SCREEN", "tesmath.calcy/.IntentReceiver")
        red_bar = False
        values = None
        while True:
            line = await self.p.read_logcat()
            line = line.decode('utf-8').strip()
            line = line[33:] # Strip off date and pid

            match = RE_CALCY_IV.match(line)
            if match:
                values = match

            match = RE_RED_BAR.match(line)
            if match:
                red_bar = True

            match = RE_SUCCESS.match(line)
            if match:
                if values is None:
                    raise CalcyIVError
                return values

            match = RE_SCAN_INVALID.match(line)
            if match:
                if red_bar:
                    raise RedBarError
                else:
                    raise CalcyIVError
        
if __name__ == '__main__':
    if platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    parser = argparse.ArgumentParser(description='Pokemon go renamer')
    parser.add_argument('--device-id', type=str, default=None,
                        help="Optional, if not specified the phone is automatically detected. Useful only if you have multiple phones connected. Use adb devices to get a list of ids.")
    parser.add_argument('--max-retries', type=int, default=5,
                        help="Maximum retries, set to 0 for unlimited.")
    parser.add_argument('--config', type=str, default="config.yaml",
                        help="Config file location.")
    parser.add_argument('--touch-paste', default=False, action='store_true',
                        help="Use touch instead of keyevent for paste.")
    parser.add_argument('--pid-name', default=None, type=str,
                        help="Create pid file")
    parser.add_argument('--pid-dir', default=None, type=str,
                        help="Change default pid directory")
    args = parser.parse_args()
    if args.pid_name is not None:
        from pid import PidFile
        with PidFile(args.pid_name, args.pid_dir) as p:
            asyncio.run(Main(args).start())
    else:
        asyncio.run(Main(args).start())
