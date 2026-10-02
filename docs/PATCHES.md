# Official patches (v1.02 and v1.03)

Both patches are WinZip self-extractors containing only a replacement `golf.exe` and text files
(no data files, no DLLs). v1.03 is cumulative: it includes all of v1.02 plus one crash fix. The disc
ships v1.03 in `Patch/SimGolf_Patch_v103.exe`, so v1.02 is not needed separately.

## Consequence for this project

The patches change game logic, which lives in `golf.exe`. A native reimplementation does not use
that executable, so there is nothing to "apply" to the data files, `Terrain.dll` or the assets this
project reads. Instead the patch notes are the behaviour target: the native game should match
v1.03 (the final shipped behaviour), not the original v1.0 disc release.

If you also want to play the original game under Wine or CrossOver, run the v1.03 patch against
your installed copy (extract it into the install folder, overwriting `golf.exe`).

## Behaviour to implement (from the official v1.02 and v1.03 notes)

v1.03
* Fix an obscure crash when selecting female golfer heads on the customisation screen (affected
  theme packs and importing custom heads).

v1.02 (3/11/2002)
* Adjusted difficulty levels; I.M. Picky visits more often, including at higher difficulties.
* Tab key no longer jumps to angry golfers (still reachable from the face bar at the bottom).
* No 50 year limit for required retirement.
* Better landmark placement: free landmarks appear in the landmark menu when Ivana donates one or
  when a happy ending occurs on the course.
* Matches and tournaments can be cancelled (wrench icon).
* A golfer can be picked up and moved elsewhere on the course, or to the clubhouse to eject them
  (eject-golfer icon after clicking the golfer).
* J.P. Bigdome offers more cash if he likes the course.
* Golfers in carts no longer complain about steep slopes.
* The golf pro (Gary Golf, or the name you give) keeps skills when you buy a new course.
* Fixed the "toilet bowl" effect on firm fairway and greens.
* Animals and golfer comments can be turned off in preferences.
* Simplified display of ranking, stars and hearts on the course name box.
* Esc clears messages instead of quitting; right-click clears messages before acting as undo.
* Fixed invalid course records, and golfers on benches not going to the tee.
