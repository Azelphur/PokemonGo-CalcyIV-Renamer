# Description
This is a small script which uses adb to send touch and key events to your phone, in combination with Calcy IV it can automatically rename all of your pokemon. This script doesn't login to the pokemon go servers using the "unofficial API" and only relies on an Android phone (sorry, iPhone users). The upside to this is that you're very unlikely to get banned for using it. The downside is that it's a lot slower, and that you can't use your phone while it's running.

# Warnings
This script essentially blindly sends touch events to your phone. If a popup appears over where the script thinks a button is, or if your phone lags, it can do unintended things. Please keep an eye on your phone while it is running. If it transfers your shiny 100% dragonite, it's because you weren't watching it.

# Usage
Simply download the files, edit config.yaml for your phone, and run `python ivcheck.py`. Make sure you are using Python >= 3.7.

# Actions
Actions allow you to define new ways of renaming your pokemon, outside of the usual Calcy IV renaming scheme. Actions are processed from first to last, and the first one to have all its conditions pass is used.

**Conditions:**
- name - The Pokemons name
- iv - The exact IV (note: this will only be set if Calcy IV has discovered an exact IV
- iv_min - The minimum possible IV (This will be set even if Calcy IV pulls an exact IV)
- iv_max - The maximum possible IV (This will be set even if Calcy IV pulls an exact IV)
- success - Whether the calcy IV scan succeeded (true/false) (Note: Will be false if pokemon is blacklisted)
- blacklist - Whether the pokemon is in the blacklist

Conditions also support the following operators:
- lt - Less than
- le - Less than or equal to
- eq - Equal to
- ne - Not equal to
- ge - Greater than or equal to
- gt - Greater than
- in - In list

**Actions:**
- rename-calcy - Rename and paste into the edit box, uses Calcy IVs naming scheme
- rename - Allows you to specify your own name for the pokemon
- favorite - Favorite the pokemon

**Examples:**
Faster rename run by skipping rename on Pokemon with <90% IVs. Rename any pokemon that failed to scan as ".FAILED" so you know which ones failed to scan, and which ones are skipped as trash.

```
actions:
  - conditions:
      success: false
    actions:
      rename: ".FAILED"
  - conditions:
      iv_max__gte: 90
    actions:
      rename-calcy:
```

Rename bad IV Abra, Gastly and Machop to ".TRADE" so you can trade them later.
```
    - conditions:
        name__in: 
          - Abra
          - Gastly
          - Machop
        iv_max__lt: 90
      actions:
        rename: ".TRADE"
```


# (probably) FAQ
* It taps in the wrong locations / doesn't work
... You probably need to edit the locations in config.yaml, it's configured for a 1080p phone.
* It's going too fast for my phone
... This was developed and tested on a OnePlus 3T, so the script runs quite fast. You can slow it down by editing config.yaml
* It's not pasting the pokemons name
... For some reason the paste key event doesn't work on some phones, use the --nopaste argument to fix it.
* Can it do multiple phones at the same time
... Sure, you just have to run multiple instances. Run `adb devices` to get the device ids for your phones, then run multiple instances of the script with --device_id=XXXXX
