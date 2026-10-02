# SimGolf data formats

Worked out from the files on a retail disc (v1.0 install, 5,659 files). "Confirmed" means the
parser in this repo reads every sample file with consistent results; "inferred" means a guess
from content and not yet verified against the game.

## Standard image / audio formats (confirmed)

| Ext | Format | Notes |
|-----|--------|-------|
| .pcx | PCX v5, RLE, 8-bit (one 24-bit file) | palette in last 769 bytes |
| .bmp | Windows BMP, uncompressed 24-bit (one 8-bit) | |
| .tga | Targa, 32-bit uncompressed | |
| .flc | Autodesk FLC/FLI animation, 8-bit | sprites; palette index 255 is the transparency key; 1, 2, 4 or 8 views per sprite (see SPRITES.md) |
| .wav | PCM RIFF WAVE | one file is really AIFF (`Sounds/Effects/Sheep 2.wav`) |
| .bik | Bink video | needs RAD's decoder or ffmpeg |
| .pal | RIFF "PAL " palette | |

FLC quirk: some chunk size fields were left uninitialised by the writer (0xCDCDCDCD). The decoder
recovers the real size (palette chunks are self-delimiting; a final chunk runs to the end of its frame).

## Character files: .chr, .glf, .pro (confirmed layout)

All little-endian, null-padded ASCII strings.

| Offset | Size | Field |
|--------|------|-------|
| 0x000 | 16 | title, for example "Heiress", "Space Cowboy", "Golf Pro" |
| 0x010 | 16 | name |
| 0x020 | 16 | raw attribute bytes (meaning not decoded yet, see below) |
| 0x030 | 512 | zero padding |
| 0x230 | 25 x 50 | dialogue slots, empty slot is all zero |
| 0x712 | 16 | zero padding, end of base record at 1826 bytes |
| 0x722 | 8 | optional ASCII tag `*PCXFILE` |
| 0x72A | rest | optional 8-bit PCX, 140x420, runs to end of file |

The PCX holds three 140x140 portraits stacked vertically: happy, neutral, angry. Its header's
unused colormap area contains uninitialised memory (often 0xCCCCCCCC), so do not trust it.

Files of exactly 1826 bytes (4 .chr and 4 .glf) are templates without a portrait.
23 files have a portrait, and in all 23 the PCX ends exactly at end of file.

Attribute bytes (0x20..0x2F): sample values are in the 0..0x20 range for the first 8 bytes,
byte 0x2C is 0..7 with bit 7 sometimes set (.chr files), and the rest are zero. Not yet mapped
to gameplay meaning. Compare the stat values in progolfers.dta below, which likely overlap.

Dialogue slots (text uses placeholders `PARTNER` and `DATA`, substituted by the game):

| Slots | Meaning |
|-------|---------|
| 0..12 | shot and course reactions (inferred: 0 to 2 look like shot-result comments) |
| 13 | crowding (confirmed from content: "Where'd all these people come from?") |
| 14, 15 | thirst: need, then satisfied (confirmed from content) |
| 16, 17 | hunger: need, then satisfied (confirmed from content) |
| 18, 19 | tiredness: need, then satisfied (confirmed from content) |
| 20..24 | unused in every shipped file |

## top10.sve (confirmed layout)

Ten records of 156 bytes (1560 bytes total):

| Offset | Size | Field |
|--------|------|-------|
| 0 | 64 | player name |
| 64 | 64 | course name |
| 128 | 4 | u32 a: sort key, descending across the ten records |
| 132 | 4 | u32 b |
| 136 | 4 | u32 c |
| 140 | 8 | two zero u32 |
| 148 | 2 | u16, zero in the sample |
| 150 | 2 | u16 tier, 0..3, rises with a |
| 152 | 4 | i32, always -1 |

Field meanings of a, b, c and tier are not known.

## .dta text tables (confirmed)

Lines starting with `*` are comments, other non-blank lines are comma separated.

* `celebrities.dta`: name, type (A..K), skin 0..3, hair 0..4, shirt 0..9, pants 0..9. The legend
  of codes is in the file's own comment header.
* `progolfers.dta`: name, body type 0..7, skin 0..3, hat 0..9, shirt 0..9, pants 0..9, then ten
  skill values as a single string of hex digits (0..F), in the order: power hitter, long driver,
  accurate driver, accurate irons, accurate putter, draw shot, fade shot, high backspin shot,
  recovery skills, luck. Many rows end with extra whitespace and a number (30..115) that rises with
  skill (inferred: hire price or rating). One row, "Brad Fiction", has a stray extra field, so
  parse defensively.

## Themes/*/*.txt conversation scripts (confirmed structure)

CRLF text. The first line is the title (leading space). The rest are blank-line separated blocks:
first line is a prompt, following indented lines are 1 to 3 reply options. File names begin with
an 8 character code of letters and `x` (for example `CMMxxMxxMaleBonding.txt`); the code is
probably which character types take part, but this is not decoded.

## Other notes

* Course geometry is not shipped on the disc; saved courses are created by the game at run time.
* Terrain textures are under `Program_Files/Data` (PCX/BMP) with per theme lighting files
  (`*Lighting.txt`: ambient, diffuse, specular RGB, then an opaque hex block, not decoded).
* `Terrain.dll` has plain C++ exports and uses OpenGL; it is the best source for the tile model.
* `golf.exe` is copy protected; this project does not touch it.

Sprite FLCs additionally carry a Firaxis header extension (views, frames per view, anchor) and one extra ring frame per view; see SPRITES.md.
