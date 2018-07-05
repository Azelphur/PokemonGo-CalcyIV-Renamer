import pokemonlib
import argparse

skip_count = 0

parser = argparse.ArgumentParser(description='Pokemon go renamer')
parser.add_argument('--device_id', type=str, default=None,
                    help="Optional, if not specified the phone is automatically detected. Useful only if you have multiple phones connected. Use adb devices to get a list of ids.")
parser.add_argument('--adb_path', type=str, default="adb",
                    help="If adb isn't on your PATH, use this option to specify the location of adb.")
parser.add_argument('--nopaste', action='store_const', const=True, default=False,
                    help="Use this switch if your device doesn't support the paste key, for example if you're using a Samsung.")
parser.add_argument('--no_rename', action='store_const', const=True, default=False,
                    help="Don't rename, useful for just loading every pokemon into calcy IV history for CSV export.")
parser.add_argument('--wait_after_error', action='store_const', const=True, default=False,
                    help="Upon calcy IV error, wait for user input.")
parser.add_argument('--max_retries', type=int, default=5,
                    help="Maximum retries, set to 0 for unlimited.")
parser.add_argument('--stop_after', type=int, default=None,
                    help="Stop after this many pokemon.")
parser.add_argument('--sleep_short', type=float, default=0.7,
                    help="Sleep duration for shorter pauses.")
parser.add_argument('--sleep_long', type=float, default=1.5,
                    help="Sleep duration for longer pauses.")
parser.add_argument('--name_line_x', type=float, default=50.74,
                    help="X coordinate (in %) of name edit button position.")
parser.add_argument('--name_line_y', type=float, default=47.97,
                    help="Y coordinate (in %) of name edit button position.")
parser.add_argument('--ok_button_x', type=float, default=86.46,
                    help="X coordinate (in %) of OK button position for keyboard input.")
parser.add_argument('--ok_button_y', type=float, default=57.08,
                    help="Y coordinate (in %) of OK button position for keyboard input.")
parser.add_argument('--save_button_x', type=float, default=51.48,
                    help="X coordinate (in %) of OK button position to name change dialog.")
parser.add_argument('--save_button_y', type=float, default=55.47,
                    help="Y coordinate (in %) of OK button position to name change dialog.")
parser.add_argument('--edit_box_x', type=float, default=92.59,
                    help="X coordinate (in %) of keyboard input field to open keyboard (used with --nopaste).")
parser.add_argument('--edit_box_y', type=float, default=88.54,
                    help="Y coordinate (in %) of keyboard input field to open keyboard (used with --nopaste).")
parser.add_argument('--edit_line_x', type=float, default=6.67,
                    help="X coordinate (in %) of keyboard input field to open edit dialog for pasting (used with --nopaste).")
parser.add_argument('--edit_line_y', type=float, default=57.29,
                    help="Y coordinate (in %) of keyboard input field to open edit dialog for pasting (used with --nopaste).")
parser.add_argument('--paste_button_x', type=float, default=11.38,
                    help="X coordinate (in %) of paste button position (used with --nopaste).")
parser.add_argument('--paste_button_y', type=float, default=64.53,
                    help="Y coordinate (in %) of paste button position (used with --nopaste).")
parser.add_argument('--calcy_button_x', type=float, default=7.40,
                    help="X coordinate (in %) of calcyIV button.")
parser.add_argument('--calcy_button_y', type=float, default=46.87,
                    help="Y coordinate (in %) of calcyIV button.")
parser.add_argument('--use_intents', type=bool, default=True,
                    help="Use intents to communicate with calcyIV.")
args = parser.parse_args()

p = pokemonlib.PokemonGo(args.device_id)
n = 0
if args.use_intents:
    p.send_intent("tesmath.calcy.ACTION_HIDE_BUTTON", "tesmath.calcy/.IntentReceiver", 0)

while args.stop_after is None or n < args.stop_after:
    if args.use_intents:
        p.send_intent("tesmath.calcy.ACTION_ANALYZE_SCREEN", "tesmath.calcy/.IntentReceiver", args.sleep_long)
    else:
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
            print("CalcyIVError " + str(args.max_retries) + " times in a row, skipping to next pokemon")
            n = n + 1
            p.swipe(97.22, 70.31, 4.62, 70.31, args.sleep_short)
            skip_count = 0
        continue

    if not args.no_rename:
        p.tap(54.91, 69.53, 0) # Dismiss Calcy IV
        p.tap(args.name_line_x, args.name_line_y, args.sleep_short) # Rename
        if args.nopaste:
            p.tap(args.edit_box_x, args.edit_box_y, args.sleep_short) # Press in the edit box
            p.swipe(args.edit_line_x, args.edit_line_y, args.edit_line_x, args.edit_line_y, args.sleep_short, 600) # Use swipe to simulate a long press to bring up copy/paste dialog
            p.tap(args.paste_button_x, args.paste_button_y, args.sleep_short) # Press paste
        else:
            p.key(279, args.sleep_short) # Paste into rename
        p.tap(args.ok_button_x, args.ok_button_y, args.sleep_short) # Press OK on edit line
        p.tap(args.save_button_x, args.save_button_y, args.sleep_long) # Press OK on Pokemon go rename dialog
    n = n + 1
    p.swipe(97.22, 70.31, 4.63, 70.31, args.sleep_short) # Swipe to next pokemon
