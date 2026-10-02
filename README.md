# simgolf-native

Clean-room native (Apple silicon friendly) port of Sid Meier's SimGolf (Firaxis, 2002).
It reads the data files from your own legitimately owned copy of the game. No game assets
or code from the original are included here, and nothing here removes or bypasses copy protection.

## Status

Steps 1 to 3 of 4 done: asset loaders, custom data formats, and a first native terrain viewer.
See docs/FORMATS.md (data formats) and docs/TERRAIN.md (terrain engine analysis).

| Format | Files on disc | Decoded OK |
|--------|---------------|------------|
| PCX (8-bit RLE, 1 x 24-bit) | 649 | 649 |
| TGA (32-bit) | 36 | 36 |
| BMP (24-bit, 1 x 8-bit) | 2631 | 2631 |
| FLC animation (8-bit) | 1893 | 1893 |
| WAV (PCM) | 320 | 319 (1 is AIFF with a .wav name) |

## Build

    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j
    build/sgtool check /path/to/extracted/game      # decode everything, report failures
    build/sgtool png   file.pcx out.png             # also tga, bmp, flc [frame]
    build/sgtool sheet anim.flc sheet.png           # contact sheet of all frames
    build/sgtool chr  Gack.chr gack                 # dump a character, writes gack_0..2.png portraits
    build/sgtool top10 top10.sve | dta file.dta | story file.txt

## Terrain viewer (macOS or Linux)

    brew install sdl2 cmake
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j
    build/sgview --game "/path/to/game/Program_Files_(ENGLISH)" --theme parkland

Keys: arrows/WASD pan, Q/E rotate, +/- or mouse wheel zoom, 1-4 themes, R new demo course, P toggle scenery, F follow the golfer,
F2 screenshot, M music, N mute, Esc quit. Tab toggles course editing (see docs/EDITING.md). `--png out.png --size 1280x800 [--time SECONDS]` renders one frame and exits.
Videos: `brew install ffmpeg`, then `build/sgplay "/path/to/game/Program_Files_(ENGLISH)/Flics/SMSG_IntroFinal.bik"` (docs/SOUND_VIDEO.md).
The course is a made-up demo. Terrain edges are blended per triangle exactly as the original
`Terrain.dll` does it (see docs/TERRAIN.md); the type grouping that decides where borders appear is my
own, because the original receives it from the protected executable.

## Getting the game data

The retail disc is an InstallShield install (data1.hdr + data1.cab + data2.cab).
Extract it with `unshield` (`brew install unshield`, then `unshield x data1.cab`).
`golf.exe` is wrapped in SafeDisc; this project never touches it.

## Findings so far

* Engine split: `golf.exe` (logic, protected), `Terrain.dll` (terrain + OpenGL rendering, plain C++
  exports such as `Terrain::tileAt`, `getElevation`, `render`), `jgl.dll` (2D layer on GDI),
  `sound.dll` (DirectSound/WinMM), `binkw32.dll` (video).
* FLC quirk: Firaxis' writer left some chunk size fields uninitialised (0xCDCDCDCD), mostly on
  palette chunks. The decoder recovers the real size (see src/flc.cpp).
* Sprite FLCs use magenta as the transparency key. Sprites have 8 camera angles per animation.
* Character files (.glf/.chr/.pro): 1826-byte record (title, name, 25 dialogue slots) plus an
  optional embedded 140x420 PCX of three portraits (happy, neutral, angry).
* Still undecoded: the 16 attribute bytes in character files, top10 fields, the story file name codes.

## Roadmap

1. Asset loaders (done)
2. Reverse the custom formats (done, a few fields unresolved, see docs/FORMATS.md)
3. Analyse Terrain.dll to reproduce the tile model and rendering (viewer with edge blending, paths, walls and a water shimmer done; the original water animation and cliff rules are not decoded)
3b. Sprite layer: FLC sprite format, views and anchors decoded, trees, a clubhouse and walking golfers in the viewer (see docs/SPRITES.md)
4. Game logic: started with a one-golfer shot loop (walk, address, swing, ball flight, putt) in sg/shot.h, with placeholder numbers; see docs/GAMELOGIC.md
5. Course editing: paint tile types, raise and lower terrain, save and load (done, basic, with path overlays; see docs/EDITING.md)
6. Club money (placeholder numbers, see docs/EDITING.md), retaining walls, water shimmer and the desert water swap (done)
7. Sound (mixer plus event sounds in sgview) and Bink video playback via ffmpeg (done, see docs/SOUND_VIDEO.md)
8. Notes from the original manual (rules only, it gives no amounts): docs/MANUAL_NOTES.md. Done from it: SGA hole classes, basic employees, golfer fun and attitude, the pathway-to-clubhouse rule
9. Facts read from a publisher-supplied golf.exe (rules and numbers only, no code copied): docs/PUBLISHER_EXE_NOTES.md
10. First playable loop: several holes, a stream of golfers paying fees, the board's debt warnings (docs/PLAYING.md). Next: menu and difficulties, buildings, ratings, memberships, tournaments, whole-game saves
