# Discord for support/development/shenaigans:
https://discord.gg/skUAWKg

# Description
This is a small script which uses adb to send touch and key events to your phone, in combination with Calcy IV it can automatically rename all of your pokemon. This script doesn't login to the pokemon go servers using the "unofficial API" and only relies on an Android phone (sorry, iPhone users). The upside to this is that you're very unlikely to get banned for using it. The downside is that it's a lot slower, and that you can't use your phone while it's running.

# Warnings
This script essentially blindly sends touch events to your phone. If a popup appears over where the script thinks a button is, or if your phone lags, it can do unintended things. Please keep an eye on your phone while it is running. If it transfers your shiny 100% dragonite, it's because you weren't watching it.

# Usage
Download the files, edit config.yaml for your phone, and run `python ivcheck.py`. Make sure you are using Python >= 3.7. Install and start https://github.com/majido/clipper on your phone (this script gets IVs by reading them back from your phones clipboard)

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
- rename-calcy - Rename and paste into the edit box, uses Calcy IVs naming scheme
- rename - Allows you to specify your own name for the pokemon
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

An example of the actions I currently use. I haven't finished fleshing it out yet, but it's a bit more advanced and gives you an idea on what you can do, the rules, in order, do the following:

- Rename any pokemon that fail to scan as ".FAILED".
- If it hasn't been appraised, and it's possibly 0 IV, appraise it.
- If its 0 or 100 IV, favorite it and rename it using calcy.
- If it has a possibility of being greater than 90 IV, appraise it.
- If it's an Abra, Kadabra, Exeggcute, Gastly, ... and it's less than 90 IV, rename it to ".TRADE" so I can easily trade it later.
- If it's a Mewtwo, Alolan Raichu, Spinda, ... use calcy to rename it.
- If it's less than 90 IV, don't bother renaming it. This saves time.
- If all else fails, use calcy to rename it.

```actions:
    - conditions:
        success: false
      actions:
        rename: ".FAILED"
    - conditions:
        iv:
        iv_min__eq: 0
        appraised: false
      actions:
        appraise:
    - conditions:
        iv__in: [0, 100]
      actions:
        favorite:
        rename-calcy:
    - conditions:
        iv:
        iv_max__ge: 90
        appraised: false
      actions:
        appraise:
    - conditions:
        name__in:
          - Abra
          - Kadabra
          - Exeggcute
          - Gastly
          - Machop
          - Ralts
          - Magikarp
          - Eevee
          - Kirlia
          - Electabuzz
        iv_max__lt: 90
      actions:
        rename: ".TRADE"
    - conditions:
        name__in: 
          - Mewtwo
          - Raichu Alolan
          - Spinda
          - Chansey
      actions:
        rename-calcy:
    - conditions:
        iv_max__le: 90
    - actions:
        rename-calcy: # Rename normally
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
