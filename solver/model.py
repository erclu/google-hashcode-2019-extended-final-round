from __future__ import annotations

# import typing as tp
# from pathlib import Path
import attr


@attr.s(frozen=True, slots=True, auto_attribs=True)
class CompiledFileProps:
    compilation_time: int = attr.ib(converter=int)
    replication_time: int = attr.ib(converter=int)


@attr.s(frozen=True, slots=True, auto_attribs=True)
class TargetFileProps(CompiledFileProps):
    deadline: int = attr.ib(converter=int)
    goal_points: int = attr.ib(converter=int)

    def score(self, completed_time: int) -> int:
        speed_points: int = self.deadline - completed_time
        return speed_points + self.goal_points if speed_points >= 0 else 0
