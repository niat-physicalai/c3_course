#!/usr/bin/env python3
"""
C2 — Generate a KiCad footprint for a through-hole breakout module.

A module soldered by its header pins needs a footprint with:
  - one plated through-hole pad per header pin (pin 1 square, others round)
  - the module's body outline on the fabrication and silkscreen layers
  - a courtyard slightly larger than the body
  - optionally, a marked rectangle on User.Drawings (for example, where an
    optical sensor sits, so the enclosure window can be lined up with it)

Edit the PARAMETERS section to match YOUR module, measured against its
mechanical drawing or a calibrated photo, then run:

    python3 C2-header-module-footprint.py

The .kicad_mod file is written into a folder called MyModules.pretty,
which you can add to KiCad as a footprint library.
"""

from pathlib import Path

# ---------------- PARAMETERS (all dimensions in mm) ----------------
NAME = "Module_21x16mm_2x4_P2.54mm"   # footprint name
BODY_W, BODY_H = 21.0, 16.0           # module body width and height
ROWS, COLS = 2, 4                     # header rows and pins per row
PITCH = 2.54                          # distance between pins in a row
ROW_SPACING = 10.16                   # distance between the two rows
DRILL, PAD = 1.0, 1.7                 # hole diameter, pad diameter
PADS_OFFSET_X, PADS_OFFSET_Y = 0.0, 0.0   # shift of pad array from body centre
COURTYARD_MARGIN = 0.25               # courtyard clearance around the body
MARKER = (5.6, 3.3, 0.0, 0.0)         # (w, h, x, y) on User.Drawings, or None
# -------------------------------------------------------------------


def rect(x1, y1, x2, y2, layer, width):
    return (f'\t(fp_rect (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f})\n'
            f'\t\t(stroke (width {width}) (type solid)) (fill no) (layer "{layer}"))\n')


def text(prop, value, y, layer):
    return (f'\t(property "{prop}" "{value}" (at 0 {y:.3f} 0) (layer "{layer}")\n'
            f'\t\t(effects (font (size 1 1) (thickness 0.15))))\n')


def pad(number, x, y):
    shape = "rect" if number == 1 else "circle"
    return (f'\t(pad "{number}" thru_hole {shape} (at {x:.3f} {y:.3f}) '
            f'(size {PAD} {PAD}) (drill {DRILL}) (layers "*.Cu" "*.Mask"))\n')


def build():
    hw, hh = BODY_W / 2, BODY_H / 2
    out = [f'(footprint "{NAME}"\n',
           '\t(version 20240108)\n',
           '\t(generator "c3_course_B5")\n',
           '\t(layer "F.Cu")\n',
           f'\t(descr "Through-hole module, {ROWS}x{COLS}, {PITCH} mm pitch, '
           f'body {BODY_W} x {BODY_H} mm")\n',
           text("Reference", "REF**", -hh - 1.5, "F.SilkS"),
           text("Value", NAME, hh + 1.5, "F.Fab"),
           '\t(attr through_hole)\n']

    # Body outline on fabrication and silkscreen layers
    out.append(rect(-hw, -hh, hw, hh, "F.Fab", 0.10))
    out.append(rect(-hw - 0.11, -hh - 0.11, hw + 0.11, hh + 0.11, "F.SilkS", 0.12))

    # Courtyard: the keep-out area other parts must not enter
    m = COURTYARD_MARGIN
    out.append(rect(-hw - m, -hh - m, hw + m, hh + m, "F.CrtYd", 0.05))

    # Optional marker, for example the optical window of a sensor
    if MARKER:
        w, h, x, y = MARKER
        out.append(rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2,
                        "User.Drawings", 0.10))

    # Pads: numbered along row 1 left to right, then row 2 left to right
    row_width = (COLS - 1) * PITCH
    number = 1
    for r in range(ROWS):
        y = PADS_OFFSET_Y - ROW_SPACING / 2 + r * ROW_SPACING if ROWS > 1 else PADS_OFFSET_Y
        for c in range(COLS):
            x = PADS_OFFSET_X - row_width / 2 + c * PITCH
            out.append(pad(number, x, y))
            number += 1

    out.append(')\n')
    return "".join(out)


if __name__ == "__main__":
    lib = Path("MyModules.pretty")
    lib.mkdir(exist_ok=True)
    path = lib / f"{NAME}.kicad_mod"
    path.write_text(build())
    print(f"Wrote {path}")
