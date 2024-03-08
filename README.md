
# telegram-to-obsidian

If you use personal telegram channel to quickly capture notes in a specific tree-like format, you can export them to your obsidian vault and merge with your day notes.

Day notes are expected to be in a structure like this: `vault_dir/chronics/2024/03/24-03-08.md`.

Also general note is created with links to all new or updated day notes.

---

### Usage:

1) Export chat history in JSON from your telegram channel. Place `result.json` into `./data/` directory.

2) Setup script constants: `PROJECT_DIR`, `VAULT_DIR`, `CHRONICS_DIR`, `LINKS_NOTE_PREFIX` (for general note name).

3) Run script `telegram_to_obsidian.py`

(or run cell in jupiter notebook `telegram_to_obsidian.ipynb`)


#### If you want to test this script beforehand:
1) Copy your notes into `./test/`, add there a directory with your vault name and inside of it - a directory with your chronics notes.

2) Stage them temporary in git (to see difference later).

3) Setup script constants for these notes.

4) Run script.

5) Check for changes (especially modifications) in git.

---

Tree-like format in telegram post:
```
Line A
Line B

Line C
.
Line C1
.
Line C2
..
Line C2_1
..
Line C2_2
.
Line C3

Line D
```


will be converted into this format for Obsidian note:
```
- Line A
    - Line B
    - Line C
        - Line C1
        - Line C2
            - Line C2_1 
            - Line C2_2
        - Line C3
    - Line D
```

Formatted posts from a day will be placed into a day note (like "2024-03-08.md") with an empty line between them. 