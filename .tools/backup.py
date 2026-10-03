"""Copy this site's tracked files to Nikos's Dropbox tree after each commit (post-commit hook).
Install once per clone:  python .tools/backup.py --install-hook
"""
import pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = pathlib.Path("C:/Users/nikmy/Dropbox/claude-hub/projects/nikmyl.github.io-backup")
if "--install-hook" in sys.argv:
    hook = ROOT / ".git" / "hooks" / "post-commit"
    hook.write_text("#!/bin/sh\npython .tools/backup.py || echo 'Dropbox backup failed; run python .tools/backup.py'\n")
    print(f"installed {hook}"); sys.exit()
files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
if DEST.exists():
    shutil.rmtree(DEST)
for f in files:
    (DEST / f).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / f, DEST / f)
head = subprocess.run(["git", "log", "-1", "--format=%h %ci %s"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
(DEST / "BACKUP_INFO.txt").write_text(f"Backup of {ROOT}\nLast commit: {head}\nRestore: copy these files into a clone of github.com/nikmyl/nikmyl.github.io\n")
print(f"backup: {len(files)} files to {DEST}")
