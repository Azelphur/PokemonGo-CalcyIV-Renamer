# Discord for support/development/shenaigans:
https://discord.gg/skUAWKg

# Description
This is a small script which uses adb to send touch and key events to your phone, in combination with Calcy IV it can automatically rename all of your pokemon. This script doesn't login to the pokemon go servers using the "unofficial API" and only relies on an Android phone (sorry, iPhone users). The upside to this is that you're very unlikely to get banned for using it. The downside is that it's a lot slower, and that you can't use your phone while it's running.

# Warnings
This script essentially blindly sends touch events to your phone. If a popup appears over where the script thinks a button is, or if your phone lags, it can do unintended things. Please keep an eye on your phone while it is running. If it transfers your shiny 100% dragonite, it's because you weren't watching it.

# Usage
- Download the files from this repository
- Install adb, make sure it's on your systems PATH, alternatively you can place adb in the same folder as main.py
- Install [clipper](https://github.com/majido/clipper) and start the service
- Install Python >=3.7 (older versions will not work)
- Run pip install -r requirements.txt
- Either change your Calcy IV renaming string to `$IV%Range$$MoveTypes$$AttIV$$DefIV$$HpIV$$Appraised$`, or change your iv_regexes setting to match your renaming scheme
- Edit config.yaml locations for your phone (The defaults are for a oneplus 3T and should work with any 1080p phone that does not have soft buttons). Each setting is an X,Y location. You can turn on Settings > Developer options > Pointer location to assist you in gathering X,Y locations. Each location setting has a corresponding screenshot in docs/locations.
- Once you've done all that, run `python ivcheck.py`

# Actions
Actions allow you to define new ways of renaming your pokemon, outside of the usual Calcy IV renaming scheme. Actions are processed from first to last, and the first one to have all its conditions pass is used.

**Conditions:**
- name - The Pokemons name
- iv - The exact IV (note: this will only be set if Calcy IV has discovered an exact IV
- iv_min - The minimum possible IV (This will be set even if Calcy IV pulls an exact IV)
- iv_max - The maximum possible IV (This will be set even if Calcy IV pulls an exact IV)
- success - Whether the calcy IV scan succeeded (true/false) (Note: Will be false if pokemon is blacklisted)
- blacklist - Whether the pokemon is in the blacklist
- appraised - Whether the pokemon has been appraised or not (true/false)
- id - The pokemons pokedex ID
- cp - The pokemons CP
- max_hp - The pokemons max hp
- dust_cost - The dust cost to power up
- level - The pokemons level (1-40)
- fast_move - The pokemons fast move (usually only visible on fully evolved pokemon)
- special_move - The pokemons special/charged move (usually only visible on fully evolved pokemon)
- gender - The pokemons gender (1 = male, 2 = female)

Conditions also support the following operators:
- lt - Less than
- le - Less than or equal to
- eq - Equal to
- ne - Not equal to
- ge - Greater than or equal to
- gt - Greater than
- in - In list

**Actions:**
- rename - Allows you to specify your own name for the pokemon. You can also use any of the above conditions as variables. For example `{name} {iv}`. In addition, there is also a {calcy} variable, which contains Calcys suggested name.
- favorite - Favorite the pokemon
- appraise - Appraise the pokemon

**Examples:**
Faster rename run by skipping rename on Pokemon with <90% IVs. Rename any pokemon that failed to scan as ".FAILED" so you know which ones failed to scan, and which ones are skipped as trash.

```
actions:
  - conditions:
      success: false
    actions:
      rename: ".FAILED"
  - conditions:
      iv_max__ge: 90
    actions:
      rename: "{calcy}"
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
... This was developed and tested on a OnePlus 3T, so the script runs quite fast. You can slow it down by editing the `waits` section in config.yaml
* It's not pasting the pokemons name
... For some reason the paste key event doesn't work on some phones, use the --nopaste argument to fix it.
* Can it do multiple phones at the same time
... Sure, you just have to run multiple instances. Run `adb devices` to get the device ids for your phones, then run multiple instances of the script with --device_id=XXXXX
