import sys
import typing as tp
from pathlib import Path

from . import solve

if __name__ == "__main__":
    args: tp.List[Path] = [Path(x).resolve() for x in sys.argv[1:]]
    solve.main(args)
