import pokemonlib
import argparse

skip_count = 0

parser = argparse.ArgumentParser(description='Pokemon go renamer')
parser.add_argument('--device_id', type=str, default=None,
                    help="Optional, if not specified the phone is automatically detected. Useful only if you have multiple phones connected. Use adb devices to get a list of ids")
parser.add_argument('--adb_path', type=str, default="adb",
                    help="If adb isn't on your PATH, use this option to specify the location of adb")
parser.add_argument('--nopaste', action='store_const', const=True, default=False,
                    help="Use this switch if your device doesn't support the paste key, for example if you're using a Samsung")
parser.add_argument('--no_rename', action='store_const', const=True, default=False,
                    help="Don't rename, useful for just loading every pokemon into calcy IV history for CSV export.")
parser.add_argument('--wait_after_error', action='store_const', const=True, default=False,
                    help="Upon calcy IV error, wait for user input")
parser.add_argument('--max_retries', type=int, default=5, help="Maximum retries, set to 0 for unlimited")
parser.add_argument('--stop_after', type=int, default=None, help="Stop after this many pokemon")
parser.add_argument('--sleep_short', type=float, default=0.7)
parser.add_argument('--sleep_long', type=float, default=1.5)
parser.add_argument('--ok_button_x', type=float, default=86.46)
parser.add_argument('--ok_button_y', type=float, default=57.08)
parser.add_argument('--edit_line_x', type=float, default=6.67)
parser.add_argument('--edit_line_y', type=float, default=57.29)
parser.add_argument('--paste_button_x', type=float, default=11.38)
parser.add_argument('--paste_button_y', type=float, default=64.53)
args = parser.parse_args()

p = pokemonlib.PokemonGo(args.device_id)
n = 0
while True:
    if args.stop_after is not None and n > args.stop_after:
        break
    p.tap(7.40, 46.87, args.sleep_long) # Calcy IV
    try:
        p.check_calcy_iv()
        skip_count = 0
    except pokemonlib.RedBarError:
        print("RedBarError, continuing")
        continue
    except pokemonlib.CalcyIVError:
        print("CalcyIVError")
        if args.wait_after_error:
            input("CalcyIVError, Press enter to continue")
        skip_count = skip_count + 1
        if skip_count > args.max_retries and args.max_retries != 0:
            print("CalcyIVError 5 times in a row, skipping to next pokemon")
            n = n + 1
            p.swipe(97.22, 70.31, 4.62, 70.31, args.sleep_short)
            skip_count = 0
        continue

    if not args.no_rename:
        p.tap(54.91, 69.53, 0) # Dismiss Calcy IV
        p.tap(50.74, 47.97, args.sleep_short) # Rename
        if args.nopaste:
            p.tap(92.59, 88.54, args.sleep_short) # Press in the edit box
            p.swipe(args.edit_line_x, args.edit_line_y, args.edit_line_x, args.edit_line_y, args.sleep_short, 600) # Use swipe to simulate a long press to bring up copy/paste dialog
            #p.tap(24.63, 50.42, args.sleep_short) # Press paste
            p.tap(args.paste_button_x, args.paste_button_y, args.sleep_short) # Press paste
        else:
            p.key(279, args.sleep_short) # Paste into rename
        p.tap(86.48, 57.08, args.sleep_short) # Press OK on edit line
        p.tap(51.48, 55.47, args.sleep_long) # Press OK on Pokemon go rename dialog
    n = n + 1
    p.swipe(97.22, 70.31, 4.63, 70.31, args.sleep_short) # Swipe to next pokemon
