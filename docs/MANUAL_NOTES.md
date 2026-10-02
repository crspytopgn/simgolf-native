# Notes from the original manual

Source: the EA UK printing of the Sid Meier's SimGolf manual (2002, 32 pages), supplied by the project owner from his own copy.
These are my own summaries with page numbers, kept because they are the only first hand description of the rules that is not
inside the protected golf.exe. **The manual gives no amounts at all** (no prices, fees, starting cash or distances), so numbers in
the code stay placeholders; what it does give is how things work.

## Modes and structure (p. 5 to 7)
* Main menu: Start New Game, Continue Saved Game, Play a Championship, Sandbox Mode, Select a Theme, Exit.
* New game: four difficulty levels, Easy, Moderate, Difficult, Impossible. Higher levels make golfer attitudes more volatile, so
  things that rarely bother golfers irritate them more. Then one of 16 properties around the world, varying in size, location and cost,
  in four themes: Parklands, Links, Desert, Tropical. You start with a fixed allotment of cash. Affordable properties show a yellow pin,
  unaffordable grey, owned magenta. Buying a new property means you cannot go back to the current one.
* Sandbox: unlimited funds, every property available.
* Championship: play a saved course as a pro golfer (saved with "Save course for championship", p. 25) for cash prizes.
* Theme packs change characters, dialogue and courses. The `Themes/` folders on the disc are these.

## Terrain (p. 8, 16, 17)
Terrain menu: Tee, Green, Fairway, Firm Fairway, Rough, Deep Rough, Sandtrap, Waste Bunker, Pot Bunker, Stream, Brush, Rocks, Water,
Trees, Scenic Trees. Hotkeys (p. 3, 4): E elevation grid, F fairway, G green/tee, T tree, P pathway, R rough, S sandtrap, W water,
- lower, = raise, Tab rotate. Right click twice removes terrain or a building.
* A tee and a hole are the minimum for a hole. The hole is placed with the Green tool; a white line joins tee and hole and shows the
  line most golfers will try (p. 14). Open a hole for business with H or by clicking its flag.
* Press Tab with the Green tool for a **tricky green**. This agrees with the terrain code found in Terrain.dll (a flag bit on the green
  tile selects the Tricky Green textures).
* **Firm fairway**: balls bounce higher and roll farther than on fairway. Rough is harder than fairway or green because the grass
  limits club and ball contact. Deep rough is harder still. A sandtrap's footing is less sure and the club cannot be grounded; a waste
  bunker has longer turf and elevation matters; a pot bunker is a deep depression with nothing to ground the club on. **Rocks deflect the
  ball at random.** Brush is difficult to recover from. Water, and streams, make a ball impossible to recover. Trees deflect long
  drives and ensnare balls; Scenic Trees do the same and also please golfers.
* Theme renames: on Desert, Rough is "Desert", Deep Rough is replaced by Rough and a Stream is a Ravine; on Links a Stream is a Burn
  and Brush is Gorse. So the `Ravine` texture set is the stream, and `Cliff` is not mentioned anywhere in the manual.
* Elevation menu (p. 8, 10): raise/lower a vertex, a square or an area, plus Analyze Golf Shot, which shows the paths golfers may take
  from a position.

## Buildings and improvements (p. 9, 18 to 20)
* Improvements: Ballwasher, Pathway, Building Lot, Benches, Scenic Bridge, Landmarks, Flower Bed, Scenic Trees.
* The Clubhouse is the core facility and comes with every property. Most buildings must be linked to it by an unbroken **pathway** to
  open; a badly connected path shows as a mud track. Moving the Clubhouse costs a replacement fee. This is a connectivity rule, and the
  editor does not enforce it.
* Ballwasher: shots after it on the hole are more accurate, but it can slow play. Benches: rest for tired golfers. Flower beds and
  landmarks lift mood. Building lots earn good money quickly and more near water, trees and fun holes.
* Facilities: Putting Green (raises imagination for golfers who already have it), Snack Bar (Pub on Links), Pro Shop (accuracy), Tennis
  Court (Stable on Links, Spa on Desert, Swim Club on Tropical; golfers start with at least a yellow attitude), Driving Range (length), Cart
  Garage (faster play), Marina (more profit from lots, a chance of a celebrity; Church on Links, Helipad on Desert), Resort Hotel (stamina),
  Airstrip (raises green fees per hole, cumulative, on Top 100 and Top 18 holes; Castle on Links, Casino on Desert, Theme Park on Tropical).
* Employees (p. 12, 20): Club Pro, Ranger, Groundskeeper, Soda Vendor, then Celebrity, Marshal, Turf Technician, Refreshment Consultant
  as skilled staff. Hiring skilled staff needs a daily fee course of six or more holes. Dandelions hurt attitude, divots and crabgrass
  appear where traffic is heavy.

## Golfers and skills (p. 10 to 12, 15, 21, 22)
* Three main skills: Length, Accuracy, Imagination.
* A golf pro has ten skills in the order of `progolfers.dta`: Power Hitter, Long Driver, Accurate Driver, Accurate Irons, Accurate
  Putter, Draw Shot, Fade Shot, High Backspin Shot, Recovery Skill, Luck. Your own pro starts with 10 skill points and each point is
  **+10 percent** in one skill, and the shot panel on p. 11 shows values like "Power Hitter +30%". The 0 to F digits in
  `progolfers.dta` are probably in the same units, but the manual does not say so (UNVERIFIED).
* Shot types: Straight (the default, a high shot for distance), Fade (curves left to right, an Imagination shot), Draw (right to left,
  Imagination), High Backspin (near the green, rolls back a little), Low Punch (low and hard under branches).
* Golfer status: fun, attitude (red, yellow, green), energy, hunger, thirst. Attitude comes from the fun rating, built from the golfer's
  comments. Happy golfers bring friends and buy memberships. Tired, hungry and thirsty golfers need benches, snack bars and soda.
* Sim-stories: two compatible golfers paired together act out a story; a happy ending adds a heart to the course window.

## Ratings and money (p. 13, 14, 22 to 24)
* Course window: funds, fun rating (average happiness) and skill rating (how often holes exercise length, accuracy and imagination).
  High ratings unlock more land (from I.M. Picky, the county commissioner), tournaments, pro-challenges and wealthy patrons who donate
  landmarks (Ivana Richman). I.M. Picky and Ivana Richman are also in the `Themes/Standard` data.
* Green fees: paid when a golfer completes a hole, primary income (p. 14).
* SGA (Sim Golf Association) evaluation: requirements are course length, number of holes, play time, minimum fun rating, variety, scenic holes,
  holes working each skill and facilities. It classifies holes as Breather (no skill needed), Freeway (length), Precise (accuracy),
  Creative (imagination), Challenge (length and accuracy), Heroic (length and imagination), Strategic (accuracy and imagination),
  Classic (all three). Top 100 holes earn higher fees, Top 18 higher again.
* Reports (F1 to F10): course status, player comments, histograph, financial report (expenses, income and profit by year), overview map,
  world screen, SGA evaluation, keyboard commands, membership roster, professional accomplishments (20 plus, each gives skill points).
* Events: SGA tournaments (when ratings are high enough, a cash boost), pro-challenges (a wager between your pro and a famous golfer, loser pays),
  snapshots.

## What this changed in the project
See docs/EDITING.md (money, hotkeys) and docs/GAMELOGIC.md (shots). Applied from this manual: the original editing hotkeys, Sandbox mode,
firm fairway run-on and rock deflection in the demo shot loop (amounts are placeholders), and the stream finding about the Ravine textures.

## What this changed (pathways, hole classes, employees)

Implemented from the manual: pathway-to-clubhouse rule, the eight SGA hole class names, the four basic employees, fun rating with red/yellow/green attitude. All numbers are placeholders because neither the manual nor any source reached so far gives them. The SimGolf fandom wiki could not be fetched (robots.txt and 402 errors), so its figures are not used.
