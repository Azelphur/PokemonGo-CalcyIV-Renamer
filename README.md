[![Youtube video showing usage](http://img.youtube.com/vi/Z2GLk0VTkIs/0.jpg)](http://www.youtube.com/watch?v=Z2GLk0VTkIs)

# Description
This is a small script which uses adb to send touch and key events to your phone, in combination with Calcy IV it can automatically rename all of your pokemon. This script doesn't login to the pokemon go servers using the "unofficial API" and only relies on an Android phone (sorry, iPhone users). The upside to this is that you're very unlikely to get banned for using it. The downside is that it's a lot slower, and that you can't use your phone while it's running.

# Warnings
This script essentially blindly sends touch events to your phone. If a popup appears over where the script thinks a button is, or if your phone lags, it can do unintended things. Please keep an eye on your phone while it is running. If it transfers your shiny 100% dragonite, it's because you weren't watching it.

# Usage
Simply download the files, and run `python ivcheck.py`, the script depends on python-pillow, so be sure to install it.

# (probably) FAQ
* It's going too fast for my phone
... This was developed and tested on a OnePlus 3T, so the script runs quite fast. You can slow it down by increasing the --sleep_short and --sleep_long arguments, which default to 0.7 and 1.5 respectively.
* It's not pasting the pokemons name
... For some reason the paste key event doesn't work on some phones, use the --nopaste argument to fix it.
* Can it do multiple phones at the same time
... Sure, you just have to run multiple instances. Run `adb devices` to get the device ids for your phones, then run multiple instances of the script with --device_id=XXXXX
