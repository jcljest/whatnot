# Whatnot break overlays for OBS

Stream overlays for running Magic: The Gathering breaks on Whatnot.

## Hybrid break board

A hybrid break has 5 slots. Each slot is one color (White, Blue, Black, Red, Green) plus 2 digits that the host assigns. The board shows viewers which color and digits each buyer owns.

![Hybrid break overlay](docs/hybrid-overlay.png)

- `breakboard/server.py` is a small local server with no dependencies beyond Python 3.
- `breakboard/control.html` is the control panel, run as an OBS dock. You type buyer names and digits here, and the overlay updates as you type. If a digit is assigned twice, it's flagged in red.
- `breakboard/overlay.html` is the on-stream board, run as an OBS browser source. It scales to the source's width.

### Setup

1. Start the server before going live:

   ```
   python breakboard/server.py
   ```

2. Add the control panel as a dock. In OBS, open **Docks → Custom Browser Docks**, then add `http://127.0.0.1:8765/control`.
3. Add the overlay to your scene. Add a **Browser** source with **Local file** unticked, set the URL to `http://127.0.0.1:8765/overlay`, and size it 1080 × 400.

The current break is saved to `breakboard/state.json`. If OBS or the server restarts mid-break, nothing is lost.

## Color break tiles

`assets/` has static SVG tiles for an 8-color break (W/U/B/R/G/Multi/Colorless/Lands). To regenerate them from one template, run:

```
python tools/build_assets.py
```
