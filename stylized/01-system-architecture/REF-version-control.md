<div style="background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 60%,#bfdbfe 100%);border:2px solid #2563eb;padding:28px 32px;border-radius:12px;margin-bottom:20px;"><div style="margin:0;font-size:32px;font-weight:700;letter-spacing:-0.5px;color:#1e3a8a;line-height:1.25;">Version Control for a Hardware Project</div></div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Knowing Exactly Which Files Made Which Board</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Course:</strong> C3 — From Problem Statement to Manufacturable Design <strong>Type:</strong> Reference page. Set it up once, before C1, and come back to it whenever you save work for the design pack. It is not a timed unit.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Why This Page Exists</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Three weeks after ordering five boards, you find a mistake and fix it in KiCad. Then the boards arrive, and one pad is in the wrong place. Was that the mistake you fixed, or a different one? Your folder holds board.kicad\_pcb, board\_new.kicad\_pcb and board\_final2.kicad\_pcb, and a Gerber zip with no date. Nobody can say which files made the boards on your desk.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Version control</strong> solves this. A tool called <strong>Git</strong> keeps a record of every saved state of your project, with a note saying what changed and when. You can go back to any earlier state, and you can mark the exact state you sent to the fab house. <strong>GitHub</strong> stores a copy of that record online, so it survives a lost laptop and others can see it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This page gives the bare minimum for one person working on one product. It does not need the command line.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Five Words You Need</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Word</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Meaning</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Repository</strong> (repo)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A project folder whose history Git records</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Commit</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">One saved state of the repo, with a message saying what changed</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Push</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Copy your new commits from your laptop to GitHub</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>Tag</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A permanent name on one commit, such as v0.1.0</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">​<strong>.gitignore</strong></td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A file listing what Git should leave out</td></tr></tbody></table>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 1: One Repository for the Whole Design Pack</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Keep <strong>everything</strong> for the product in one repo: specification, schematic, board, CAD, firmware and documents. Then one commit can record a board change together with the case change it caused, and the two can never drift apart.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Lay it out like the design pack G asks for, so the repo is the pack:</div>

```text
my-product/
├── README.md
├── .gitignore
├── 01-spec-and-architecture/
├── 02-hardware-architecture/
├── 03-part-selection/
├── 04-schematic-and-pcb/        ← KiCad project folder
├── 05-firmware-design/
├── 06-firmware-and-simulation/  ← PlatformIO project
├── 07-mechanical/               ← Fusion .f3d and .step exports
├── 08-manufacturing/            ← the Gerber zip you ordered with
└── …                           ← the remaining G files (version 2, reviews, verification log)
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's public repository [5] is organised by kind of file rather than by design-pack section: firmware/, pcb/ (the KiCad project, its symbol library, the board STEP and a 3d models folder), fabrication/ and asset/ (images), with a README at the top. Either layout works, as long as it is one repo and the README explains it.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 2: Set It Up With GitHub Desktop</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>GitHub Desktop</strong> is a free app that does everything on this page with buttons [1].</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Make a free GitHub account, install GitHub Desktop, and sign in.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. <strong>File → New Repository.</strong> Give it your product's name, choose where it lives on your laptop, and tick <strong>Initialize this repository with a README</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Click <strong>Publish repository</strong>. Choose <strong>private</strong> until you are happy for others to see it; you can make it public later.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Create the numbered folders from Step 1 inside it, and add the .gitignore from Step 4.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">From now on, save your KiCad project, Fusion exports and firmware <strong>inside</strong> this folder.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">KiCad 10 also has Git built in: in the Project Manager, right-click a file and use <strong>Version Control</strong> to commit and push [3]. It works, but it only sees the KiCad project. GitHub Desktop sees the whole pack, so use that.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 3: Commit Small, Commit Often</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Each time you finish a piece of work that makes sense on its own, commit it:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Open GitHub Desktop. The <strong>Changes</strong> tab lists every file you changed since the last commit.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. Untick any file that does not belong in this commit.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Write a <strong>summary</strong> saying what changed and why, then click <strong>Commit to main</strong>.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Click <strong>Push origin</strong> to copy the commit to GitHub.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A good message lets you find a change months later without opening any file:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Weak</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Better</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">update</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Move SDA/SCL from 21/22 to D4/D5</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">pcb changes</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Widen 3V3 track to 0.6 mm; DRC clean</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">final</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Case: wall 1.5 → 2.0 mm after E3 audit</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Natural moments to commit in this course:</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">After</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Message names</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">ERC reaches zero errors (C1)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The schematic is checked</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A footprint is drawn and checked (C2)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Which footprint, and what it was checked against</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">DRC reaches zero errors (C3)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The board is checked</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">A case change in Fusion (E0–E4), with fresh .f3d and .step exports</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">What changed in the case</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The fabrication files are generated (F1)</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The revision being ordered</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">A commit is cheap. Ten small commits are easier to understand, and to undo, than one big one.</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 4: Decide What Git Ignores</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Commit the files you <strong>made</strong>. Leave out the files your tools <strong>make for themselves</strong>, which change on every save and mean nothing to anyone else.</div>

<table style="margin:16px auto;border-collapse:collapse;"><thead><tr><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Commit</th><th style="background:#2563eb;color:#ffffff;font-weight:700;padding:10px 28px;border:1px solid #1e40af;text-align:center;">Ignore</th></tr></thead><tbody><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">KiCad: .kicad\_pro, .kicad\_sch, .kicad\_pcb, your project libraries (.kicad\_sym, .pretty folders), sym-lib-table, fp-lib-table</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">KiCad's backups (.history/ in KiCad 10 [3], \*-backups/ in older versions), lock files, fp-info-cache</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">3D models you use, and the board's exported .step</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Fusion: .f3d and .step exports</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">— (Fusion keeps its own history in its cloud; it is not in Git)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Firmware source, platformio.ini</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The build folder (.pio/)</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Documents, spreadsheets, images</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">Your operating system's clutter files</td></tr><tr><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">The exact Gerber zip you sent to the fab</td><td style="padding:9px 28px;border:1px solid #bfdbfe;background:#eff6ff;text-align:center;">—</td></tr></tbody></table>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">Copy this into a file called .gitignore at the top of your repo:</div>

```text
# KiCad
.history/
*-backups/
*.lck
fp-info-cache
_autosave-*
\#auto_saved_files\#

# PlatformIO
.pio/

# Operating systems
.DS_Store
Thumbs.db
```

<div style="text-align:justify;line-height:1.7;margin:10px 0;">KiCad's .kicad\_prl file holds only your local view settings, such as which layers are visible. Committing it is harmless; ignore it too (\*.kicad\_prl) if it keeps showing up as changed.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's repository has a .gitignore inside its PlatformIO folder but none at the top, so KiCad's lock and cache files are not ruled out for the pcb/ folder. A top-level .gitignore like the one above fixes that.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">​<strong>Large files.</strong> GitHub warns about files over 50 MB and refuses files over 100 MB [2]. A board STEP with every 3D model can be several megabytes; that is fine. If a model is huge, use a simpler one or a stand-in box (E2).</div>

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Step 5: Tag the Version You Send to the Fab</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">This is the step that answers the question at the top of the page. When you order boards:</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. Generate the fabrication files (F1) and commit them, with the Gerber zip, in one commit.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. In GitHub Desktop, open the <strong>History</strong> tab, right-click that commit and choose <strong>Create Tag</strong> [4]. Name it after the board's revision, for example v0.1.0.</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Push, so the tag reaches GitHub.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">Use the <strong>same</strong> revision in three places: the tag, the schematic's title block (C1) and the silkscreen text (C3). Then anyone holding a board can read its revision and find the exact files that made it.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">esp\_watch's board says version 0.1.0 on its silkscreen, and its schematic's title block says revision 0.1.0. Its repository has <strong>no tags</strong>, so nothing in the history marks which commit the ordered boards were made from. Tagging that commit v0.1.0 would close the gap.</div>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">When a later change is ordered, tag it v0.2.0, and so on. Never move or reuse a tag.</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Things You Can Leave for Later</div>

<ul style="text-align:justify;line-height:1.7;padding-left:22px;"><li style="margin:6px 0;">​<strong>Branches</strong> let you try a change on a side line without touching the main one. Useful in a team; not needed alone.</li><li style="margin:6px 0;">​<strong>Pull requests</strong> are how a team reviews a branch before merging it. Not needed alone.</li><li style="margin:6px 0;">​<strong>Merge conflicts</strong> happen when two people change the same lines. KiCad and Fusion files merge badly, so in a team, agree who edits the board and who edits the case at any one time.</li></ul>

<div style="text-align:justify;line-height:1.7;margin:10px 0;">The Git book covers all three when you need them [6].</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">Checklist</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. The whole design pack is in one Git repository, pushed to GitHub. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. The repo has a .gitignore, and no KiCad backup, lock or cache files are committed. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. Fusion .f3d and .step exports are committed alongside the KiCad project. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. Every commit message says what changed. — Y/N</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. The commit you sent to the fab house is tagged, and the tag matches the title block and the silkscreen. — Y/N</div>

---

<div style="background:linear-gradient(90deg,#dbeafe 0%,#ffffff 100%);border-left:6px solid #1e3a8a;border-radius:6px;padding:10px 16px;margin:34px 0 16px 0;font-size:22px;font-weight:700;color:#1e3a8a;">References</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">1. GitHub. GitHub Desktop documentation. https://docs.github.com/en/desktop</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">2. GitHub. About large files on GitHub (warning above 50 MB, block above 100 MB). https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">3. KiCad. KiCad 10.0 documentation (project backups in the .history folder; Git integration in the Project Manager). In the course's reference/kicad/kicad.pdf. https://docs.kicad.org/10.0/en/kicad/kicad.html</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">4. GitHub. Managing tags in GitHub Desktop. https://docs.github.com/en/desktop/managing-commits/managing-tags-in-github-desktop</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">5. esp\_watch repository. https://github.com/niat-physicalai/esp\_watch</div>

<div style="text-align:justify;line-height:1.7;margin:14px 0 8px 0;">6. Chacon, S. and Straub, B. Pro Git, 2nd edition. https://git-scm.com/book/en/v2</div>
