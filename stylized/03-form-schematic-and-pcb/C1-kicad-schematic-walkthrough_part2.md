<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 10: Annotate</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Every symbol needs a unique reference. KiCad fills them in as you place symbols, as long as <strong>Annotate Automatically</strong> in the left toolbar is on.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/automatically_annotate.png" alt="The Annotate Automatically toggle, in the left toolbar" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Annotate Automatically toggle, in the left toolbar</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">After copying and pasting, you may see U? or two parts with the same reference. Click <strong>Annotate Schematic</strong> in the top toolbar, keep the defaults, and click <strong>Annotate</strong>.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/annotate_schematic.png" alt="The Annotate Schematic button, in the top toolbar" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Annotate Schematic button, in the top toolbar</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 11: Assign Footprints</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each symbol needs a <strong>footprint</strong>: the pattern of copper pads its part is soldered to. Click <strong>Assign Footprints</strong> in the top toolbar.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W12.png" alt="The Assign Footprints button" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Assign Footprints button</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The window has three panes:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Pane</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Shows</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">You</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Left</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Footprint libraries, such as Button\_Switch\_THT for through-hole switches and ...\_SMD libraries for surface-mount parts</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Click a library to list its footprints on the right</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Middle</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Every symbol on the sheet: reference, value and the footprint assigned so far</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Click the symbol you are assigning</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Right</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The footprints in the chosen library</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Double-click one to assign it to the selected symbol</td></tr></tbody></table>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W122.png" alt="Assign Footprints on esp_watch: libraries on the left, the seven symbols in the middle, footprints on the right" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Assign Footprints on esp\_watch: libraries on the left, the seven symbols in the middle, footprints on the right</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Before you double-click, check the footprint. Right-click it and choose <strong>View Selected Footprint</strong> to see its pads and size [5]. Compare them with the part's datasheet, and check that the part you will buy matches that size. The <strong>Footprint Filters</strong> buttons at the top narrow the right pane, for example to footprints with the symbol's pin count; type in the box beside them to narrow it further.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W123.png" alt="Viewing a footprint before assigning it" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Viewing a footprint before assigning it</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>Apply, Save Schematic &amp; Continue</strong> to keep going, or <strong>OK</strong> when every symbol has a footprint.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's assignments:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Symbol</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Footprint</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U1, XIAO ESP32-C3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">xiao:xiao\_esp32c3 (downloaded)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">esp:MAX30102 module (drawn by the author)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MPU-6050 module</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">esp:GY-521 MPU6050 MODULE FOOTPRINT</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SSD1306 OLED</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">oled:128x64OLED</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SW1, SW2</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Button\_Switch\_THT:SW\_PUSH\_6mm (KiCad library)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SW3</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Button\_Switch\_THT:SW\_Slide-03\_Wuerth-WS-SLTV\_10x2.5x6.4\_P2.54mm (KiCad library)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Where the library has no footprint for your part, assign it later: drawing and checking one is C2's job. Before C3, every symbol must have a footprint.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 12: Run ERC</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click <strong>Electrical Rules Checker</strong> in the top toolbar (or <strong>Inspect → Electrical Rules Checker</strong>), then <strong>Run ERC</strong>.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/Electrical_rule_checker.png" alt="The Electrical Rules Checker button" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Electrical Rules Checker button</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each problem is listed in the dialog, and an arrow marks it on the sheet. Click a line to jump to its arrow [5].</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W13.png" alt="ERC on esp_watch: four power-input errors and one library warning, with arrows marking them on the sheet" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">ERC on esp\_watch: four power-input errors and one library warning, with arrows marking them on the sheet</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">ERC knows each pin's <strong>type</strong> (power input, output, bidirectional and so on), set in the symbol, and checks that connected pins make sense together. It also catches unconnected pins, unannotated symbols and labels that connect to nothing. These are the errors you will meet:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">ERC message (paraphrased)</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Usual cause</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Fix</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Input power pin not driven by any output power pin</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power arrives through a pin KiCad does not see as a source: a battery, a connector, or a module's own regulator</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Confirm the net really is powered, then place a <strong>PWR\_FLAG</strong> (from the power library) on it [5]</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Pin not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A pin with no wire and no flag</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Wire it, or add a no-connect flag if it is unused on purpose</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Symbol not annotated</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U? left after copying</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Annotate (Step 10)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Label not connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A typo, or a label not touching its wire</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fix the spelling or the position</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Two outputs connected</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Two pins that both drive the net</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check the design, and each pin's type in the symbol (C2)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Symbol doesn't match copy in library (warning)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The symbol in the schematic differs from the one in its library, often because the library was edited afterwards</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Right-click the symbol, <strong>Update Symbol from Library</strong>, if the library version is the right one</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Run on esp\_watch with every test on, ERC shows four errors and one warning. All four errors are "Input Power pin not driven": on the XIAO's B+ pin and on three power symbols. The XIAO's own regulator makes the 3.3 V and the battery feeds +3.7V, but the symbols type those pins as power <strong>inputs</strong>, and nothing on the sheet is typed as a power <strong>output</strong>, so ERC sees no source. The warning says the MPU-6050 symbol no longer matches its library copy.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The circuit is fine. The author checked by hand that the 3.3 V and battery nets never touch each other or GND, then set ERC to ignore those two tests. The clean result below lists them under <strong>Ignored Tests</strong>.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W14.png" alt="The clean ERC run: 0 errors, 0 warnings, with the ignored tests counted on the right tab" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The clean ERC run: 0 errors, 0 warnings, with the ignored tests counted on the right tab</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">There are two honest ways out of a power-input error:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Place a PWR\_FLAG</strong> (from the power symbols, <strong>P</strong>) on each net that really is powered. It tells ERC the net has a source, and every other check keeps working. This is the better fix, and the one to use on any board bigger than a few modules.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Ignore the test</strong>, as esp\_watch does: right-click the error and choose to ignore that kind of violation. Do it only after checking by hand that each supply reaches the pins it should, that no two different voltages are joined, and that no supply touches GND. Write that check down.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Aim for <strong>zero errors</strong>. You may exclude a single violation by right-clicking it, but write down why. Never change pin types to make errors go away: the errors disappear, and so does every check ERC could have made.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>ERC does not know what your circuit is for.</strong> A schematic can pass with SDA and SCL swapped, or a button on a boot pin. That is why you tick each connection against the B3 pin map as you draw.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 13: Notes, and the BOM</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Fabrication notes.</strong> Add text (the <strong>T</strong> tool) for anything a builder must know that the wiring cannot show.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's schematic carries no notes. One fact from B3 is invisible in its wiring and deserves one: MAX30102\_module1 must be the <strong>black</strong> (3.3 V) module, because the green one pulls the bus to 1.8 V.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Test points</strong> are small pads where a probe can touch during bring-up. Add one (symbol TestPoint) on each power rail, ground and each bus line if the board has room.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>BOM.</strong> <strong>Tools → Generate Bill of Materials</strong> lists every symbol's reference, value and footprint [5]. This list is the starting point for the costed BOM in F0, which is why the Value fields matter.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Tool Reference</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The tools this unit used, as they appear in KiCad 10. Hover over any button in KiCad to see its name and hotkey.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Tool</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Key</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Use it to</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/Place_symbols.png">Place Symbols</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Place a part</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/Place_power_symbols.png">Place Power Symbols</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">P</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Place +3V3, GND, PWR\_FLAG</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/Draw_wires.png">Draw Wires</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">W</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Connect two pins</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/C1-W08.png">Place Net Labels</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">L</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Name a net; same names connect</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/C1-W09.png">Place No Connect Flags</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Q</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Mark a pin unused on purpose</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/Place_junctions.png">Place Junctions</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">J</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Join wires where KiCad did not</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/highlight_nets.png">Highlight Nets</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Light up every pin on one net</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/annotate_schematic.png">Annotate Schematic</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Give every symbol a unique reference</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/C1-W12.png">Assign Footprints</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Link symbols to pad patterns</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/Electrical_rule_checker.png">Electrical Rules Checker</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Check the drawing for errors</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/symbol_editor.png">Symbol Editor</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Draw your own symbol (C2)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">!<a href="../assets/kicad/schematic_view/tools/switch_to_pcb_editor.png">Switch to PCB Editor</a></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Open the board (C3)</td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Applying What You Have Learned</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Draw your own product's schematic, following the steps above.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. <strong>Create the project</strong> and fill in the page settings, with revision 0.1. Put the project folder in a Git repository.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>Place every part</strong> from your B4 BOM. For a module with no symbol, use a generic connector with the right pin count, or draw one now with C2.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. <strong>Wire and label</strong> every connection in your B2 interface table, ticking each one off. Use the table's names for the labels.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. <strong>Flag every unused pin</strong> with a no-connect flag.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. <strong>Fill in Reference, Value and Footprint</strong> for every symbol, then annotate. Leave a footprint blank only if C2 will draw it, and note which.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. <strong>Run ERC to zero errors.</strong> Write a reason beside every exclusion.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. <strong>Add one fabrication note</strong> for anything a builder could get wrong, and generate the BOM.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Deliverable:</strong> your KiCad project (.kicad\_pro and .kicad\_sch), a screenshot of the clean ERC result, and the generated BOM, saved in your design pack as C1-schematic/.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Self-Check</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open your schematic and answer each item Y or N.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The title block shows the product name, a date and a revision. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Every connection in your B2 interface table appears in the schematic, and each was ticked off. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Every signal net has a label whose name matches the interface table exactly. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every unused pin has a no-connect flag. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. No reference ends in ?, and no two symbols share a reference. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Every symbol has a Value, and every symbol has a footprint (or a note saying C2 will draw it). — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">7. ERC reports zero errors, and every exclusion has a written reason. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">8. The project folder is committed to a Git repository. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Check Your Understanding</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>1.</strong> You label the microcontroller's data pin SDA and the sensor's data pin I2C\_SDA. What happens?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. KiCad joins them, because both names contain "SDA".</li><li style="margin:6px 0;">B. ERC changes one name to match the other.</li><li style="margin:6px 0;">C. They stay two separate nets.</li><li style="margin:6px 0;">D. They connect on the PCB but not in the schematic.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> Labels connect only when their names match exactly. <strong>A</strong> and <strong>B</strong> describe matching that KiCad does not do. <strong>D</strong> is impossible: the PCB's nets come from the schematic. Highlight Nets shows the problem at once.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>2.</strong> A pushbutton already has wires to two pins. You want to move it a little to the left and keep it connected. Which key do you use?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. M</li><li style="margin:6px 0;">B. G</li><li style="margin:6px 0;">C. R</li><li style="margin:6px 0;">D. X</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Drag (G) moves the symbol and keeps its wires attached. <strong>A</strong>, move, leaves the wires behind, so the pins come loose. <strong>C</strong> rotates and <strong>D</strong> mirrors; neither moves the part.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>3.</strong> Your board is powered from a USB connector symbol whose pins are all passive. ERC reports "Input power pin not driven" on +5V. You have checked that the connector really does supply +5V. What is the right fix?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Change every module's power pin type to passive.</li><li style="margin:6px 0;">B. Exclude the error without a note.</li><li style="margin:6px 0;">C. Delete the +5V power symbols and use wires instead.</li><li style="margin:6px 0;">D. Place a PWR\_FLAG on the +5V net.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> A PWR\_FLAG tells ERC the net is driven, which is true. <strong>A</strong> removes information, so ERC can no longer catch a real unpowered part. <strong>B</strong> leaves an unexplained exclusion. <strong>C</strong> changes nothing about what drives the net.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>4.</strong> Your microcontroller's pin D7 is unused. What should the schematic show?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A no-connect flag on D7.</li><li style="margin:6px 0;">B. D7 deleted from the symbol.</li><li style="margin:6px 0;">C. D7's type changed to passive.</li><li style="margin:6px 0;">D. A wire from D7 to ground.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> The flag records that the pin is unused on purpose, and ERC accepts it. <strong>B</strong> makes the symbol disagree with the real part. <strong>C</strong> hides the pin from ERC instead of recording a decision. <strong>D</strong> ties an I/O pin to ground, which could short it if the firmware ever drives it high.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>5.</strong> A schematic passes ERC with zero errors. Which of these could it still contain?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. A symbol with reference U?</li><li style="margin:6px 0;">B. SDA and SCL swapped at one sensor</li><li style="margin:6px 0;">C. A pin with no wire and no flag</li><li style="margin:6px 0;">D. A label touching no wire</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>B.</strong> Both nets connect pins of sensible types, so ERC sees nothing wrong. Only checking against your pin map catches it. <strong>A</strong>, <strong>C</strong> and <strong>D</strong> are all things ERC reports.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>6.</strong> You select an 8-pin module symbol in Assign Footprints, and the right pane lists thousands of footprints. What narrows it fastest?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Scrolling the right pane until the module's footprint appears.</li><li style="margin:6px 0;">B. Deleting unused libraries from the left pane.</li><li style="margin:6px 0;">C. Re-annotating the schematic.</li><li style="margin:6px 0;">D. The pin-count filter, then the text box.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>D.</strong> The pin-count filter keeps only 8-pad footprints, and the text box narrows those further. <strong>A</strong> works but wastes time. <strong>B</strong> changes your library setup for every project. <strong>C</strong> has nothing to do with footprints.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>7.</strong> After copying a sensor section and pasting it, ERC reports two symbols named U3. What do you do?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. Run Annotate Schematic.</li><li style="margin:6px 0;">B. Delete one of the sensors.</li><li style="margin:6px 0;">C. Exclude the error.</li><li style="margin:6px 0;">D. Rename the net labels.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>A.</strong> Annotation gives every symbol a unique reference. <strong>B</strong> removes a part you need. <strong>C</strong> would leave two parts with the same reference, which confuses the BOM and the board. <strong>D</strong> changes nets, not references.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>8.</strong> Your OLED module is sold in two versions: one with pin 1 as GND, one with pin 1 as VCC. Your footprint suits the GND-first version. Which fabrication note prevents a failure?</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">A. "The display address is 0x3C."</li><li style="margin:6px 0;">B. "Connect the OLED's supply pin to the 3.3 V rail, never to 5 V."</li><li style="margin:6px 0;">C. "Fit only the GND-first OLED version."</li><li style="margin:6px 0;">D. "All grounds are common."</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Answer</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>C.</strong> The pin order is invisible in the schematic, but fitting the wrong version reverses the supply. <strong>A</strong> and <strong>D</strong> are true but cannot be got wrong by a builder. <strong>B</strong> is already shown by the wiring.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What Comes Next</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Some of your parts have no symbol or footprint in KiCad's libraries. In <a href="C2-symbols-and-footprints.md">C2</a> you draw them, and check the ones you download.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. KiCad. Getting Started in KiCad, version 10.0 (new project, schematic editor basics, placing symbols, wiring, labels, annotation, footprint assignment, ERC). https://docs.kicad.org/10.0/en/getting\_started\_in\_kicad/getting\_started\_in\_kicad.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. KiCad. PCB Editor reference manual, version 10.0. https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. KiCad. Download. https://www.kicad.org/download/</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. niat-physicalai. esp\_watch (KiCad project in pcb/esp\_Watch/). https://github.com/niat-physicalai/esp\_watch</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. KiCad. Schematic Editor reference manual, version 10.0 (no-connect flags, PWR\_FLAG, Assign Footprints, ERC, Generate Bill of Materials). https://docs.kicad.org/10.0/en/eeschema/eeschema.html</div>
