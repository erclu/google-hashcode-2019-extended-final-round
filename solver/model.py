from __future__ import annotations

import typing as tp
from pathlib import Path

import attr


@attr.s(slots=True, frozen=True, auto_attribs=True)
class CompiledFile:
    name: str
    compilation_time: int = attr.ib(converter=int)
    replication_time: int = attr.ib(converter=int)
    raw_dependencies: tp.List[str]

    @classmethod
    def from_rows(cls, first_row: str, second_row: str) -> CompiledFile:
        name, compilation_time, replication_time = first_row.split(" ")

        dep_list: tp.List[str]
        if len(second_row) > 1:
            dep_list = second_row[2:].rstrip("\n").split(" ")
        else:
            dep_list = []

        return cls(name, compilation_time, replication_time, dep_list)

    @staticmethod
    def find_in(
      compiled_files_list: tp.List[CompiledFile], name: str
    ) -> CompiledFile:
        """gets the compiled file with given name from a list"""
        return next(filter(lambda x: x.name == name, compiled_files_list))


@attr.s(slots=True, frozen=True, auto_attribs=True)
class TargetFile:
    name: str
    deadline: int = attr.ib(converter=int)
    goal_points: int = attr.ib(converter=int)

    def score(self, completion_time: int) -> int:
        speed_points: int = self.deadline - completion_time
        return speed_points + self.goal_points if speed_points >= 0 else 0

    @classmethod
    def from_row(cls, row: str) -> TargetFile:
        return cls(*row.split(" "))


@attr.s(slots=True, auto_attribs=True)
class Server:
    number: int = attr.ib(converter=int)
    available_files: tp.Set[CompiledFile] = attr.ib(default=attr.Factory(set))


@attr.s(slots=True, frozen=True, auto_attribs=True)
class Step:
    compiled_file: CompiledFile
    server: Server


@attr.s(slots=True, auto_attribs=True)
class CompilationSteps:
    steps: tp.List[Step] = attr.ib(default=attr.Factory(list), init=False)
    score: int = attr.ib(default=0, init=False)
    targets: tp.Set[TargetFile] = attr.ib(default=attr.Factory(set))

    def add_step(self, step: Step) -> None:
        self.steps.append(step) #pylint: disable=no-member

    def save(self, outfile: Path) -> None:
        submission_rows: tp.List[str] = ["{}".format(len(self.steps))] + [
          "{} {}".format(x.compiled_file.name, x.server.number)
          for x in self.steps #pylint: disable=not-an-iterable
        ]

        outfile.write_text("\n".join(submission_rows))
