<!-- ASSIGNABLE: version-control · home: 01-system-architecture -->

# Version Control for a Hardware Project
## Knowing Exactly Which Files Made Which Board

**Course:** C3 — From Problem Statement to Manufacturable Design
**Type:** Reference page. Set it up once, before C1, and come back to it whenever you save work for the design pack. It is not a timed unit.

---

### Why This Page Exists

Three weeks after ordering five boards, you find a mistake and fix it in KiCad. Then the boards arrive, and one pad is in the wrong place. Was that the mistake you fixed, or a different one? Your folder holds `board.kicad_pcb`, `board_new.kicad_pcb` and `board_final2.kicad_pcb`, and a Gerber zip with no date. Nobody can say which files made the boards on your desk.

**Version control** solves this. A tool called **Git** keeps a record of every saved state of your project, with a note saying what changed and when. You can go back to any earlier state, and you can mark the exact state you sent to the fab house. **GitHub** stores a copy of that record online, so it survives a lost laptop and others can see it.

This page gives the bare minimum for one person working on one product. It does not need the command line.

---

## Five Words You Need

| Word | Meaning |
|---|---|
| **Repository** (repo) | A project folder whose history Git records |
| **Commit** | One saved state of the repo, with a message saying what changed |
| **Push** | Copy your new commits from your laptop to GitHub |
| **Tag** | A permanent name on one commit, such as `v0.1.0` |
| **`.gitignore`** | A file listing what Git should leave out |

---

## Step 1: One Repository for the Whole Design Pack

Keep **everything** for the product in one repo: specification, schematic, board, CAD, firmware and documents. Then one commit can record a board change together with the case change it caused, and the two can never drift apart.

Lay it out like the design pack G asks for, so the repo *is* the pack:

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

<!-- REFPRODUCT:START -->
esp_watch's public repository [5] is organised by kind of file rather than by design-pack section: `firmware/`, `pcb/` (the KiCad project, its symbol library, the board STEP and a `3d models` folder), `fabrication/` and `asset/` (images), with a README at the top. Either layout works, as long as it is one repo and the README explains it.
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: VC-02
caption: esp_watch's repository on GitHub: one repo for firmware, board, fabrication files and images
brief: GitHub web page for niat-physicalai/esp_watch, the file list at the top level
  (asset, fabrication, firmware, pcb, README.md) with the README starting to render below.
  Light theme. Crop to the file list and the first lines of the README.
-->

## Step 2: Set It Up With GitHub Desktop

**GitHub Desktop** is a free app that does everything on this page with buttons [1].

1. Make a free GitHub account, install GitHub Desktop, and sign in.
2. **File → New Repository.** Give it your product's name, choose where it lives on your laptop, and tick **Initialize this repository with a README**.
3. Click **Publish repository**. Choose **private** until you are happy for others to see it; you can make it public later.
4. Create the numbered folders from Step 1 inside it, and add the `.gitignore` from Step 4.

From now on, save your KiCad project, Fusion exports and firmware **inside** this folder.

KiCad 10 also has Git built in: in the Project Manager, right-click a file and use **Version Control** to commit and push [3]. It works, but it only sees the KiCad project. GitHub Desktop sees the whole pack, so use that.

## Step 3: Commit Small, Commit Often

Each time you finish a piece of work that makes sense on its own, commit it:

1. Open GitHub Desktop. The **Changes** tab lists every file you changed since the last commit.
2. Untick any file that does not belong in this commit.
3. Write a **summary** saying what changed and why, then click **Commit to main**.
4. Click **Push origin** to copy the commit to GitHub.

<!-- MEDIA
type: screenshot
id: VC-01
caption: A commit in GitHub Desktop: the changed files, and a message that says what changed
brief: GitHub Desktop, Changes tab, on the esp_watch repo (or a copy). Two or three changed
  files ticked on the left, for example esp_Watch.kicad_sch and esp_Watch.kicad_pcb. Summary
  box filled in with a message like "Move SW2 to D9; reroute button line". The Commit to main
  button visible. Light theme.
-->

A good message lets you find a change months later without opening any file:

| Weak | Better |
|---|---|
| `update` | `Move SDA/SCL from 21/22 to D4/D5` |
| `pcb changes` | `Widen 3V3 track to 0.6 mm; DRC clean` |
| `final` | `Case: wall 1.5 → 2.0 mm after E3 audit` |

Natural moments to commit in this course:

| After | Message names |
|---|---|
| ERC reaches zero errors (C1) | The schematic is checked |
| A footprint is drawn and checked (C2) | Which footprint, and what it was checked against |
| DRC reaches zero errors (C3) | The board is checked |
| A case change in Fusion (E0–E4), with fresh `.f3d` and `.step` exports | What changed in the case |
| The fabrication files are generated (F1) | The revision being ordered |

A commit is cheap. Ten small commits are easier to understand, and to undo, than one big one.

## Step 4: Decide What Git Ignores

Commit the files you **made**. Leave out the files your tools **make for themselves**, which change on every save and mean nothing to anyone else.

| Commit | Ignore |
|---|---|
| KiCad: `.kicad_pro`, `.kicad_sch`, `.kicad_pcb`, your project libraries (`.kicad_sym`, `.pretty` folders), `sym-lib-table`, `fp-lib-table` | KiCad's backups (`.history/` in KiCad 10 [3], `*-backups/` in older versions), lock files, `fp-info-cache` |
| 3D models you use, and the board's exported `.step` | — |
| Fusion: `.f3d` and `.step` exports | — (Fusion keeps its own history in its cloud; it is not in Git) |
| Firmware source, `platformio.ini` | The build folder (`.pio/`) |
| Documents, spreadsheets, images | Your operating system's clutter files |
| The exact Gerber zip you sent to the fab | — |

Copy this into a file called `.gitignore` at the top of your repo:

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

KiCad's `.kicad_prl` file holds only your local view settings, such as which layers are visible. Committing it is harmless; ignore it too (`*.kicad_prl`) if it keeps showing up as changed.

<!-- REFPRODUCT:START -->
esp_watch's repository has a `.gitignore` inside its PlatformIO folder but none at the top, so KiCad's lock and cache files are not ruled out for the `pcb/` folder. A top-level `.gitignore` like the one above fixes that.
<!-- REFPRODUCT:END -->

**Large files.** GitHub warns about files over 50 MB and refuses files over 100 MB [2]. A board STEP with every 3D model can be several megabytes; that is fine. If a model is huge, use a simpler one or a stand-in box (E2).

## Step 5: Tag the Version You Send to the Fab

This is the step that answers the question at the top of the page. When you order boards:

1. Generate the fabrication files (F1) and commit them, with the Gerber zip, in one commit.
2. In GitHub Desktop, open the **History** tab, right-click that commit and choose **Create Tag** [4]. Name it after the board's revision, for example `v0.1.0`.
3. Push, so the tag reaches GitHub.

Use the **same** revision in three places: the tag, the schematic's title block (C1) and the silkscreen text (C3). Then anyone holding a board can read its revision and find the exact files that made it.

<!-- REFPRODUCT:START -->
esp_watch's board says `version 0.1.0` on its silkscreen, and its schematic's title block says revision 0.1.0. Its repository has **no tags**, so nothing in the history marks which commit the ordered boards were made from. Tagging that commit `v0.1.0` would close the gap.
<!-- REFPRODUCT:END -->

<!-- MEDIA
type: screenshot
id: VC-03
caption: Tagging the commit that was sent to the fab house
brief: GitHub Desktop, History tab, right-click menu on a commit with "Create Tag…" highlighted,
  and the tag dialog with "v0.1.0" typed in. If the esp_watch repo is tagged, use it;
  otherwise a practice repo with a commit message like "Fabrication files for rev 0.1.0".
  Light theme.
-->

When a later change is ordered, tag it `v0.2.0`, and so on. Never move or reuse a tag.

---

## Things You Can Leave for Later

- **Branches** let you try a change on a side line without touching the main one. Useful in a team; not needed alone.
- **Pull requests** are how a team reviews a branch before merging it. Not needed alone.
- **Merge conflicts** happen when two people change the same lines. KiCad and Fusion files merge badly, so in a team, agree who edits the board and who edits the case at any one time.

The Git book covers all three when you need them [6].

---

## Checklist

1. The whole design pack is in one Git repository, pushed to GitHub. — Y/N
2. The repo has a `.gitignore`, and no KiCad backup, lock or cache files are committed. — Y/N
3. Fusion `.f3d` and `.step` exports are committed alongside the KiCad project. — Y/N
4. Every commit message says what changed. — Y/N
5. The commit you sent to the fab house is tagged, and the tag matches the title block and the silkscreen. — Y/N

---

## References

1. GitHub. *GitHub Desktop documentation*. https://docs.github.com/en/desktop
2. GitHub. *About large files on GitHub* (warning above 50 MB, block above 100 MB). https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
3. KiCad. *KiCad 10.0 documentation* (project backups in the `.history` folder; Git integration in the Project Manager). In the course's `reference/kicad/kicad.pdf`. https://docs.kicad.org/10.0/en/kicad/kicad.html
4. GitHub. *Managing tags in GitHub Desktop*. https://docs.github.com/en/desktop/managing-commits/managing-tags-in-github-desktop
5. esp_watch repository. https://github.com/niat-physicalai/esp_watch
6. Chacon, S. and Straub, B. *Pro Git*, 2nd edition. https://git-scm.com/book/en/v2
