# ACTIONS Examples

**This folder contains several actions examples, from the very simple ones to ridiculously complicated.**

Use them as is, or as guideline to build your own config.yaml.

To use them, replace all your `actions:` block with one of these, with careful not to replace the following block, `iv_regexes`.

## Sorting Table

**This is the order in which Pokemon displays pokémons when sorting by A-Z. Useful for working out a custom order you'd like to view your pokémons.**

_For Gboard users, the character in parenthesis indicates which key on Gboard contains the character in question (with tap&hold)._

- `꩜ ` _(Special @. Not available on Gboard)_
- `!`
- `#`
- `$`
- `%`
- `&`
- `*`
- `@`
- `,`
- `.`
- `?`
- `^`
- `_`
- `¡` _(Inside key `!`)_
- `¿` _(Inside key `?`)_
- `“` _(Inside key `"`)_
- `›` _(Inside key `'`)_
- `‽` _(Inside key `?`)_
- `+`
- `⁺` _(Superscript Plus. Not available on Gboard)_
- `=`
- `±`
- `»` _(Inside key `"`)_
- `§` _(Inside key `¶`)
- `¶`
- `÷`
- `×`
- `∅` _(Inside key `0`)_
- `√`
- `≈` _(Inside key `=`)_
- `↑` _(Inside key `^`)_
- `→` _(Inside key `^`)_
- `↓` _(Inside key `^`)_
- `←` _(Inside key `^`)_
- `⇆` _(Double Arrow. Not available on Gboard)_
- `·` _(Inside key `-`)_
- `†` _(Inside key `*`)_
- `‡` _(Inside key `*`)_
- `•`
- `‰`
- `☀️` _(It's a sun emoji)_
- `★` _(Inside key `*`)_
- `♠` _(Inside key `•`)_
- `♣` _(Inside key `•`)_
- `♥` _(Inside key `•`)_
- `♦` _(Inside key `•`)_
- `✂️` (Emoji)
- `✓`
- `∞` _(Inside key `=`)_
- Numbers
- Letters
- `μ` _(Inside key `π`)_
- `Π` _(Inside key `π`)_
- `π`
- `Ω` _(Inside key `π`)_


### Per device differences

**Characters above with `[A]` or similar at the end means that the order changes depending on the device. Yeah...**

The letter between the brackets is the device's "type" _(more like mood)_, so if your phone follows pattern [A], you should disregard characters labeled as [B]. In other words, it's either one, or the other.


### True character length:

**If you get lots of _Please choose another pokemon name_ when renaming, that means that some of your symbols are too big, and the string is exceeding 12 characters. Though they might look like the occupy a single space, they're actually composed of several unicode elements, making them bigger than they appear, and thus making PoGo unhappy.**

**Below follows a list with each character *true length* from the list above.**

_Keep in mind that 0.5 doesn't mean you can have 24 characters that long, but when counting the whole string it does apply (i.e.: you can't have 24 letters-long name if PoGo's counting is higher than 12 chars.)._

- `꩜ : 2.0`
- `!: 0.5`
- `#: 0.5`
- `$: 0.5`
- `%: 0.5`
- `&: 0.5`
- `*: 0.5`
- `@: 0.5`
- `,: 0.5`
- `.: 0.5`
- `?: 0.5`
- `^: 0.5`
- `_: 0.5`
- `¡: 1.0`
- `¿: 1.0`
- `“: 1.5`
- `›: 1.5`
- `‽: 1.5`
- `+: 0.5`
- `⁺: 1.5`
- `=: 0.5`
- `±: 1.0`
- `»: 1.0`
- `§: 1.0`
- `¶: 1.0`
- `÷: 1.0`
- `×: 1.0`
- `∅: 1.5`
- `√: 1.5`
- `≈: 1.5`
- `↑: 1.5`
- `→: 1.5`
- `↓: 1.5`
- `←: 1.5`
- `⇆: 1.5`
- `μ: 1.0`
- `·: 1.0`
- `†: 1.5`
- `‡: 1.5`
- `•: 1.5`
- `‰: 1.5`
- `☀️: 3.0`
- `★: 1.5`
- `♠: 1.5`
- `♣: 1.5`
- `♥: 1.5`
- `♦: 1.5`
- `✂️: 3.0`
- `✓: 1.5`
- `€: 1.5`
- `∞: 1.5`
- `Numbers: 0.5`
- `∞: 1.5`
- `Letters: 0.5`
- `Π: 1.0`
- `π: 1.0`
- `Ω: 1.0`
