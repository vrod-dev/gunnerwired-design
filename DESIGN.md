# GunnerWired design guide

How GunnerWired graphics are built. Everything marked **Locked** is agreed and
should not change without Vino's say-so.

Last updated: 18 November 2026 (posters, table poster, profile picture and X header)

## 1. Format (Locked)

- Portrait poster, 1080 × 1350 px (4:5).
- Draw at 2× (2160 × 2700) and scale down, so edges stay smooth.
- Two colourways: **home** for Arsenal home games, **away** for away games.

## 2. Background: bolt pattern with gradient fade (Locked)

Every poster uses the same background: a two-tone bolt pattern covering the
whole card, fading into a solid dark colour on the left where the text sits.

### The pattern

A repeating zigzag "bolt", rebuilt as clean geometry from Vino's original
pattern artwork. Two flat tones only: no outline, no third colour.

Geometry, in pattern units (1 unit = 1.1 card px):

| Property | Value | Meaning |
| --- | --- | --- |
| Tooth | (161, 127) | One full tooth along a bolt: right 161, down 127 |
| Shallow stroke | (260.3, −153.4) | Rises to the right at about 30° |
| Steep stroke | (−99.3, 280.5) | Drops down and slightly left, about 70° |
| Bolt-to-bolt sweep | (−176, 210) | Step from one bolt to the next |
| Bolt share | 0.47 | Bolt takes 47% of each repeat, the gap 53% |
| Zoom | 1.1 card px per unit | |

The pattern is drawn in code from these numbers, so it repeats endlessly and
can be rendered at any size. Do not paste in a bitmap of it.

### The fade

The pattern fades out towards the left, along the same slant as the bolts.

- Strength at a point (x, y) in card px:
  `t = (x − (250 + 0.52 × (675 − y))) / 640`, clamped to 0..1,
  then eased with smoothstep: `t² × (3 − 2t)`.
- At mid height the pattern starts to appear at x = 250 and reaches full
  strength at x = 890.
- Left of the fade is solid background colour.

### Colours

The background colour is also the gap between bolts, so the bolts appear to
grow out of the background.

| | Home | Away |
| --- | --- | --- |
| Background and fade colour | Deep red `#640716` | Navy `#0F1838` |
| Bolt colour | Red `#CE1126` | Blue `#224096` |
| Text | White `#FFFFFF` | White `#FFFFFF` |
| Accent | Yellow `#FFCC00` | Yellow `#FFCC00` |

### Don't

- Don't add outlines, a third pattern colour, textures or glass effects.
- Don't put the pattern on a white or light background.
- Don't change the zoom, angles or fade without updating this file.

## 3. Type (Locked)

Two typefaces, both free for commercial use (SIL Open Font License) and
bundled with the bot:

| Typeface | Used for |
| --- | --- |
| **League Gothic** | Everything big: the vertical title, scores, team names, kick-off time |
| **Poppins Medium** | Everything small: "GUNNERWIRED", labels, the competition line, the channel link |

- All text is in capitals.
- League Gothic: letter-spacing 2 px on names, 4 px on the title.
- Poppins: always small (19 to 24 px) with wide letter-spacing (6 px).
- White text, with yellow reserved for the accents listed in section 4.

## 4. Layout (Locked)

### Shared by every poster

- **Vertical title** on the right: League Gothic, white, reading bottom to
  top. It runs the full height of the card and sits flush on the top, bottom
  and right edges. It is positioned by the base of the flat letters, so the
  letters themselves touch the edge.
- **Brand**, top left: the cannon mark in yellow, 120 px wide, with
  "GUNNERWIRED" beside it in Poppins.
- **Left column**: starts 64 px from the left edge and stops 40 px short of
  the title.
- **Footer**: a thin yellow rule at y = 1086, the competition line below it
  in Poppins, and the channel link in yellow at y = 1262.

### Full time

- Title: "FULL TIME".
- Two rows, home team first: a huge League Gothic score (360 px) with the
  team name beneath it (up to 104 px).
- Arsenal's score is yellow; the opponent's is white.
- Extra time or a penalty shoot-out is noted on a second small line under
  the competition line.

### Matchday

- Title: "MATCHDAY".
- Both team names stacked in League Gothic (up to 150 px) with a small
  yellow "V" between them.
- "KICK-OFF" label, then the UK kick-off time as the big yellow number
  (330 px), then "UK TIME · HOME" or "UK TIME · AWAY".

### Weekly table

- Title: "THE TABLE". Always the home (red) colourway.
- Posted with Monday's round-up.
- Rows: the top six, plus Arsenal on an extra row if they are outside it.
- Columns: position, team, played, goal difference, points, all in League
  Gothic at 62 px, with small Poppins column labels above.
- Arsenal's row is yellow; the others are white. A faint rule sits under
  each row.
- The footer's small line gives the next fixture.

### News poster (news_card.py)

- Title runs full height on the right, like every poster. It must be one of
  the fixed titles (LATEST NEWS, TEAM NEWS, TRANSFER NEWS, INJURY NEWS,
  MATCH PREVIEW, MATCH REPORT, STAT ATTACK, ON THIS DAY, THE BIG QUESTION,
  ACADEMY NEWS, WOMEN'S TEAM). Short words like "NEWS" alone make the title
  too thick, so they are not allowed.
- Kicker: small yellow Poppins label above the headline.
- Headline: League Gothic, white, wrapped to the left column, as large as
  fits (up to 150 px). Write it in our own words, never copied from a source.
- One small line in the footer for context.
- Home colourway by default; away for stories about away games or rumours.

### Fitting rules

- Both team names always share one size. If either is too long for the left
  column, both shrink together.
- Double-digit scores shrink to fit the column.

## 5. Logo mark (Locked)

- The GunnerWired cannon with the **wire**: a zigzag signal leaving the
  muzzle. This is the only version of the logo. An earlier variant with
  frequency bars is retired and must not be used.
- On posters, the header and the profile picture: single flat colour, the
  accent yellow.
- Never use the club crest or any part of it.

## 6. Profile picture and X header (Locked)

### Profile picture (Telegram channel, bot, X)

- Square, 1024 × 1024 px, designed for a circular crop.
- The cannon in yellow, centred, 600 px wide.
- Background: the bolt pattern with a radial gradient, faintest in the
  centre and strengthening gradually all the way to the rim. No hard ring
  where the pattern starts.
- Available in red (home) and navy (away).

### X header

- 1500 × 500 px.
- Background: the left-to-right fade used on the posters, solid colour on
  the left and pattern on the right.
- Content: the cannon, "GUNNERWIRED" in League Gothic (132 px) and the
  tagline "ARSENAL NEWS · RESULTS · FIXTURES" in Poppins.
- All content stays inside the safe area, x 360 to 1140 and y 150 to 420,
  centred between X's back and search buttons. Outside that area X crops
  about 125 px off each side on phones, covers the top with the status bar,
  and covers the bottom-left corner with the profile picture.

## 7. What we can't use

GunnerWired is an unofficial fan channel that earns money, so nothing owned by
the club or its kit makers goes into the graphics:

- the club crest or cannon artwork
- actual kit patterns or shirt designs
- the club's custom typeface
- photos of players, unless separately licensed

Club colours, and the general attitude of bold kit-style graphics, are fine.

## 8. Where this applies

- Full-time result posters (in the bot)
- Matchday posters (in the bot)
- Weekly table poster (in the bot)
- News posters for X (news_card.py, used by the daily scheduled task)
- Profile picture and X header (set by hand)
