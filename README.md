# Pokemon Radical Red v4.1 Team Exporter

Live app: **https://rad-red-41-team-exporter.streamlit.app/**

Export every Pokemon from your Radical Red v4.1 save file — party **and** all PC boxes — straight into Showdown paste format.

## What it exports

- Species & Nickname
- Ability (primary / secondary / hidden)
- EVs / IVs (only non-default values shown)
- Nature
- Moves
- Held Item
- Level (party Pokemon)

## What it does **not** export

- Gender
- Happiness
- Shiny status

## Usage

1. Open the web app (link above) or run locally with `streamlit run radred_team_extractor.py`
2. Upload your 128 KB `.sav` file
3. All party and box Pokemon are displayed automatically in Showdown format
4. Click **Download All (.txt)** to save everything to a text file

### iOS users

If the file picker won't show your `.sav` file, rename it to `.bin` or use the **Files** app to locate it.

## Showdown integration

Paste the exported text directly into the [Radical Red Teambuilder](https://play.radicalred.net/teambuilder) or the [Showdown damage calculator](https://calc.pokemonshowdown.com/).

> Double-check your sets before relying on damage calcs — minor discrepancies are possible.

## Credits

Huge thanks to [Bulbapedia](https://bulbapedia.bulbagarden.net/) for the GBA save data structure documentation.
