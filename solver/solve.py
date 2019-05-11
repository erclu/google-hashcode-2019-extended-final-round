import typing as tp
from pathlib import Path

from tqdm import tqdm

from . import model


def parse_file(filename: Path) -> tp.Tuple[tp.List[model.CompiledFile],
                                           tp.List[model.TargetFile],
                                           int,
                                           ]:
    lines: tp.List[str] = filename.read_text(encoding="UTF-8").split("\n")[:-1]

    comp_files_number: int
    target_files_number: int
    servers_number: int
    comp_files_number, target_files_number, servers_number = (
      int(x) for x in lines.pop(0).split(" ")
    )

    assert len(lines) == comp_files_number*2 + target_files_number

    comp_files_raw: tp.List[str] = lines[:comp_files_number*2]
    target_files_raw: tp.List[str] = lines[-target_files_number:]

    compiled_files: tp.List[model.CompiledFile] = [
      model.CompiledFile.from_rows(x, y)
      for x, y in zip(comp_files_raw[:-1:2], comp_files_raw[1::2])
    ]

    target_files: tp.List[model.TargetFile] = [
      model.TargetFile.from_row(row)
      for row in tqdm(target_files_raw, ascii=True)
    ]

    return compiled_files, target_files, servers_number


def _solve(filename: Path) -> None:
    compiled_files, target_files, servers_number = parse_file(filename)

    print(*compiled_files, sep="\n")
    print(*target_files, sep="\n")
    print(servers_number)


def main(files: tp.List[Path]) -> None:
    for file in files:
        _solve(file)
