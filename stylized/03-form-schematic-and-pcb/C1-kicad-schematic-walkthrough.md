<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">C1 — KiCad Walkthrough: From Pin Map to Schematic</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Drawing a Real Board's Schematic, One Step at a Time</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Module:</strong> 3 — Form Factor, Schematic and PCB <strong>Time:</strong> ~1.5 hours · <strong>You will produce:</strong> a KiCad schematic of your own product that passes ERC with zero errors</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">From Breadboard to Board</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Your circuit works on a breadboard. To turn it into a board that a fab house can make, you need two drawings: a <strong>schematic</strong>, which says what connects to what, and a <strong>PCB layout</strong>, which says where the copper goes. KiCad makes both, and the schematic comes first, because the layout is built from it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This unit walks through esp\_watch's real schematic in KiCad 10, step by step, then asks you to do the same for your own product. It shows only the tools you need to draw one board. Everything else is in the official KiCad manuals [1][2]; you will not need most of it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What You Will Be Able to Do After This Reading</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Create</strong> a KiCad project and set up its schematic sheet.</li><li style="margin:6px 0;">​<strong>Place</strong> symbols, power symbols, wires, net labels and no-connect flags, using their hotkeys.</li><li style="margin:6px 0;">​<strong>Fill in</strong> each symbol's reference, value and footprint, and annotate the schematic.</li><li style="margin:6px 0;">​<strong>Run</strong> ERC and <strong>resolve</strong> the errors you will meet, down to zero.</li><li style="margin:6px 0;">​<strong>Check</strong> the finished schematic against your B3 pin map, connection by connection.</li></ul>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Before You Start</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">You need three things open:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">What</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Where</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">KiCad 10</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Free, from kicad.org [3]. Windows, macOS and Linux.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your <strong>B3 pin map</strong> and <strong>B2 interface table</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your design pack</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">esp\_watch's KiCad project, to compare against</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb/esp\_Watch/ in the public repository [4]. Download the repository as a ZIP, or use KiCad's <strong>File → Clone Project from Repository</strong></td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>The schematic is a transcription.</strong> Every connection was already decided in B2 and B3. Here you copy those decisions into KiCad; you do not make new ones. Keep the pin map beside KiCad and tick off each connection as you draw it. If you find yourself moving a signal to a different pin, stop: update B3 first, with a reason, then draw it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">What esp\_watch's schematic contains</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">One A4 sheet, drawn in KiCad 10:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Item</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">On esp\_watch</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Microcontroller</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U1, the XIAO ESP32-C3</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Modules</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">MAX30102 (black), MPU-6050 (GY-521 style), SSD1306 OLED</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Switches</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SW1 and SW2 pushbuttons, SW3 slide switch in the battery line</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Power symbols</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">+3V3, GND, and +3.7V on the battery side of SW3</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Labels</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">SDA and SCL, as global labels</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">No-connect flags</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">16, one on every unused pin</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Title block</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ESP\_WATCH, revision 0.1.0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Resistors</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">None. The I²C pull-ups are already on the modules, and the buttons use the XIAO's internal pull-ups</td></tr></tbody></table>

<div style="text-align:center;margin:16px 0;"><img src="https://raw.githubusercontent.com/niat-physicalai/esp_watch/main/asset/pcb/Schematic.png" alt="The esp_watch schematic in KiCad" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The esp\_watch schematic in KiCad</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Keep your project in a Git repository from the first save, so every later change can be undone and the version you send to the fab house is recorded. If you have not set one up yet, do it now with <a href="../01-system-architecture/REF-version-control.md">Version Control for a Hardware Project</a>; it takes about fifteen minutes.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 1: Create the Project</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Open KiCad. The window that appears is the <strong>Project Manager</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Click <strong>File → New Project</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Choose the <strong>default</strong> template and click <strong>OK</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Pick a folder, name the project (for example my\_product), and keep <strong>Create a new folder for the project</strong> ticked. Click <strong>Save</strong>.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/new_project.png" alt="File menu in KiCad&#x27;s Project Manager, with New Project highlighted" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">File menu in KiCad's Project Manager, with New Project highlighted</div></div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/project_type.png" alt="Choosing the default project template" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Choosing the default project template</div></div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/choosing_project_location.png" alt="Choosing where to save the project" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Choosing where to save the project</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">KiCad creates three files with the project's name. You will use all three:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">File</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Holds</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.kicad\_pro</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Project settings</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.kicad\_sch</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The schematic (this unit)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">.kicad\_pcb</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The board (C3)</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">KiCad 10 also keeps automatic backups in a hidden .history folder. Leave it out of Git.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 2: Open the Schematic Editor</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Double-click the .kicad\_sch file in the Project Files list, or click <strong>Schematic Editor</strong> on the right.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/opening_schematic.png" alt="Opening the schematic file from the Project Manager" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Opening the schematic file from the Project Manager</div></div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/schematic_view_screen.png" alt="The Schematic Editor with an empty A4 sheet" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Schematic Editor with an empty A4 sheet</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The <strong>right toolbar</strong> holds the drawing tools. The <strong>left toolbar</strong> holds display settings such as the grid and units. The <strong>top toolbar</strong> holds the checks (annotate, ERC, footprints).</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Moving around:</strong> drag with the middle or right mouse button to pan, and use the scroll wheel to zoom. On a laptop touchpad, change this in <strong>Preferences → Preferences → Mouse and Touchpad</strong> [1]. <strong>Help → List Hotkeys</strong> shows every shortcut.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 3: Set Up the Sheet</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Right-click an empty spot on the sheet and choose <strong>Properties…</strong> (<strong>E</strong>), or use <strong>File → Page Settings</strong>.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/Drawing_sheet_properties1.png" alt="Right-click on the sheet, then Properties" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Right-click on the sheet, then Properties</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Fill in the title, date and revision, and choose the paper size. These print in the title block in the bottom-right corner, and they tell anyone holding a printout which version it is.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/Drawing_sheet_properties2.png" alt="The Page Settings dialog: paper size on the left, title block fields on the right" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Page Settings dialog: paper size on the left, title block fields on the right</div></div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/Drawing_sheet_table.png" alt="The title block it fills in" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The title block it fills in</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch uses A4, title ESP\_WATCH, revision 0.1.0. Raise the revision every time a version goes to the fab house.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 4: Place the Symbols (A)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Press <strong>A</strong>, or click the <strong>Place Symbols</strong> button in the right toolbar.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/Place_symbols.png" alt="The Place Symbols button, hotkey A" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Place Symbols button, hotkey A</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The <strong>Choose Symbol</strong> dialog opens. Type in the search box, pick the symbol, click <strong>OK</strong>, then click on the sheet to place it.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/Symbol_selection_screen.png" alt="The Choose Symbol dialog, showing a symbol and its default footprint" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Choose Symbol dialog, showing a symbol and its default footprint</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">KiCad's libraries hold the chips and generic parts: SW\_Push for a pushbutton, R for a resistor, Conn\_01x04 for a 4-pin header. Most <strong>modules</strong> are not there, because each seller makes a slightly different board. esp\_watch's three modules use symbols the author drew, kept in a project library (symbol.kicad\_sym). <a href="C2-symbols-and-footprints.md">C2</a> shows how to draw one. Until you have, you can place a generic connector with the right pin count as a stand-in.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Once a symbol is on the sheet, these keys arrange it:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Key</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Does</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>M</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move. The item comes away from its wires, which stay where they were.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>G</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Drag. The wires stay attached and stretch to follow. Dragging a selected item with the mouse does the same.</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>R</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Rotate</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>X</strong> / <strong>Y</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Mirror</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Del</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Delete</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Esc</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Cancel the current tool</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Put the microcontroller in the middle, and each module on the side where its pins face the microcontroller. A schematic arranged this way needs few crossing wires.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 5: Add Power Symbols (P)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Press <strong>P</strong>, or click the <strong>Place Power Symbols</strong> button.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/Place_power_symbols.png" alt="The Place Power Symbols button, hotkey P" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Place Power Symbols button, hotkey P</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The dialog now shows only power symbols. Place +3V3 and GND wherever a pin needs them.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/Power_symbol_selection_screen.png" alt="The Choose Power Symbol dialog" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Choose Power Symbol dialog</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Power symbols with the same name are connected,</strong> even with no wire between them [1]. Every GND on the sheet is one net. This keeps the drawing clean: each module gets its own small +3V3 and GND symbol instead of long supply wires.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 6: Draw the Wires (W)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Press <strong>W</strong>, or click the <strong>Draw Wires</strong> button.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/Draw_wires.png" alt="The Draw Wires button, hotkey W" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Draw Wires button, hotkey W</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click a pin to start the wire, and click another pin to finish it. To go round a corner, <strong>click once while drawing</strong>: the wire up to that point is fixed, and you carry on left, right, up or down from there. Double-click to end a wire in empty space, and press <strong>Esc</strong> to cancel. Hovering over an unconnected pin also starts a wire when you click it.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/C1-W07.gif" alt="Wiring SW1 between the XIAO&#x27;s D10 pin and ground" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Wiring SW1 between the XIAO's D10 pin and ground</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The small circle on a pin disappears once it is connected. Where a wire meets the middle of another wire, KiCad adds a <strong>junction</strong> dot automatically. If two wires cross without a dot, they are <strong>not</strong> connected. Press <strong>J</strong> (<strong>Place Junctions</strong>) to add one by hand only when KiCad has not.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/Place_junctions.png" alt="The Place Junctions button, hotkey J" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Place Junctions button, hotkey J</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 7: Name the Signals with Net Labels (L)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Press <strong>L</strong>, or click <strong>Place Net Labels</strong>.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W08.png" alt="The Place Net Labels button, hotkey L" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Place Net Labels button, hotkey L</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The <strong>Label Properties</strong> dialog opens first. Type the net's name in <strong>Label</strong> and click <strong>OK</strong>. A label needs a name: the name is what makes the connection. To place several labels in a row, tick <strong>Multiple label input</strong> and type one name per line.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W082.png" alt="The Label Properties dialog, where you type the net&#x27;s name" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Label Properties dialog, where you type the net's name</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The label now follows the cursor. Click to drop it so its small connection point sits <strong>on a wire</strong>. A label floating next to a wire connects nothing.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W083.png" alt="Placing SCL on the wire from the XIAO&#x27;s D5 pin, with SDA already on D4" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Placing SCL on the wire from the XIAO's D5 pin, with SDA already on D4</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Labels with the same name are connected</strong> [1], so SDA on the microcontroller and SDA on each module form one net, with no wire running between them.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Take every name from your <strong>B2 interface table</strong>, and spell it the same way in the schematic, the PCB and the firmware. The names follow the net onto the board, where they appear on every pad.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A name must match <strong>exactly</strong>. SDA and I2C\_SDA are two different nets, and nothing joins them. After labelling, click the <strong>Highlight Nets</strong> tool and click a wire: every pin on that net lights up, which is a quick way to check.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/highlight_nets.png" alt="The Highlight Nets button" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Highlight Nets button</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch labels only SDA and SCL, and wires its buttons directly. It uses <strong>global labels</strong> for them: the flag-shaped labels at the end of each module's SDA and SCL wire and at the XIAO's D4 and D5. On one sheet a global label behaves exactly like a net label. On your own board, label every signal from the interface table, such as BTN\_NEXT and BTN\_PREV, so the PCB editor shows readable names instead of Net-(U1-D10).</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A one-sheet board needs only <strong>net labels</strong> (<strong>L</strong>). <strong>Global labels</strong> (<strong>Ctrl+L</strong>) connect across several sheets of a larger design; their dialog adds a <strong>Shape</strong> (input, output, bidirectional) that ERC can check. Either works on one sheet. Pick one kind and use it for every net, so the drawing reads the same everywhere.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 8: Mark the Unused Pins (Q)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Press <strong>Q</strong>, or click <strong>Place No Connect Flags</strong>, and click each pin that is unused on purpose. The <strong>no-connect flag</strong> (a small ) tells ERC that the pin is meant to be left alone [1].</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W09.png" alt="The Place No Connect Flags button, hotkey Q" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">The Place No Connect Flags button, hotkey Q</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch has 16: eight on the XIAO (D0–D3, D6–D8 and VUSB), the module pins it does not use, such as both sensors' interrupt pins (the firmware polls the sensors instead), and the slide switch's spare pin.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W092.png" alt="No-connect flags on the MAX30102 module&#x27;s unused pins: its second GND, RD, IRD and INT" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">No-connect flags on the MAX30102 module's unused pins: its second GND, RD, IRD and INT</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Do not delete an unused pin from a symbol, and do not change its type to hide it. The flag records a decision; the other two hide one.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 9: Fill In Each Symbol's Fields (E)</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Click a symbol to select it; it is highlighted, as below. Then press <strong>E</strong>, or double-click it.</div>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/selected_symbol.png" alt="esp_watch&#x27;s MAX30102 module, selected" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">esp\_watch's MAX30102 module, selected</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The <strong>Symbol Properties</strong> dialog has four fields that matter:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Field</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Put in it</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Why</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Reference</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">U1, U2, SW1, R1</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The short name on the board's silkscreen and in the BOM</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Value</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The part: XIAO ESP32C3, MAX30102 module, black, 4.7k</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Becomes the BOM's description</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Footprint</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The pad pattern on the board</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Links the symbol to copper (Step 11)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Datasheet</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A link to the datasheet</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One click from the schematic to the source</td></tr></tbody></table>

<div style="text-align:center;margin:16px 0;"><img src="../assets/kicad/schematic_view/tools/C1-W10.png" alt="Symbol Properties for esp_watch&#x27;s MAX30102 module: Reference, an empty Value, and its Footprint" style="width:100%;max-width:700px;border-radius:8px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.08);display:block;margin:0 auto;"><div style="font-size:13px;color:#64748b;margin-top:7px;text-align:center;">Symbol Properties for esp\_watch's MAX30102 module: Reference, an empty Value, and its Footprint</div></div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's three module symbols carry long references (MAX30102\_module1, MPU-6050\_module1, SSD1306OLED1) and empty Value fields. On your board, use the standard short prefix (U for a module or IC) and put the part name in Value, so the BOM in F0 reads cleanly.</div>

---

<div style="background:#eff6ff;border-left:4px solid #2563eb;border-radius:8px;padding:12px 16px;margin:16px 0;text-align:center;line-height:1.7;"><div style="font-weight:700;color:#1e40af;">This cookbook will be continued in Part 2.</div></div>
