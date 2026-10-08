"""Re-run the calling script under the repo's .venv Python when started from another interpreter,
so `python3 tools/<tool>.py …` works without activating the venv. Import it before any third-party module."""
import os
import sys
from pathlib import Path

_venv = Path(__file__).resolve().parent.parent / ".venv"
_py = _venv / "bin" / "python"
if _py.exists() and Path(sys.prefix).resolve() != _venv.resolve() and not os.environ.get("DECK_KIT_REEXEC"):
    os.environ["DECK_KIT_REEXEC"] = "1"     # guard against a loop if the venv is broken
    os.execv(str(_py), [str(_py), *sys.argv])
