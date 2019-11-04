import typing as tp
from pathlib import Path

import networkx as nx
from tqdm import tqdm

from . import model


def parse_file(filename: Path) -> tp.Tuple[tp.List[str],
                                           tp.List[str],
                                           tp.List[str],
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

    raw_compiled_files: tp.List[str] = lines[:comp_files_number*2 - 1:2]
    raw_dependencies_list: tp.List[str] = lines[1:comp_files_number*2:2]
    raw_target_files: tp.List[str] = lines[-target_files_number:]

    return (
      raw_compiled_files,
      raw_dependencies_list,
      raw_target_files,
      servers_number,
    )


def build_graph(
  raw_compiled_files: tp.List[str],
  raw_dependencies_list: tp.List[str],
  raw_target_files: tp.List[str],
) -> nx.DiGraph:
    dep_graph: nx.DiGraph = nx.DiGraph()

    for compiled_file, dependencies in tqdm(zip(
      raw_compiled_files, raw_dependencies_list), ascii=True):

        name, compilation_time, replication_time = compiled_file.split(" ")
        dep_graph.add_node(
          name,
          props=model.CompiledFileProps(compilation_time, replication_time),
          is_target=False
        )
        if len(dependencies) > 2:
            destinations = dependencies[2:].split(" ")
            for dependency in destinations:
                dep_graph.add_edge(name, dependency)

    for target_file in raw_target_files:
        name, deadline, goal_points = target_file.split(" ")

        props: model.CompiledFileProps = dep_graph.nodes[name]["props"]

        dep_graph.nodes[name]["props"] = model.TargetFileProps(
          props.compilation_time, props.replication_time, deadline, goal_points
        )
        dep_graph.nodes[name]["is_target"] = True

    return dep_graph


def _solve(filename: Path) -> None:
    (
      raw_compiled_files,
      raw_dependencies_list,
      raw_target_files,
      servers_number,
    ) = parse_file(filename)

    dep_graph = build_graph(
      raw_compiled_files, raw_dependencies_list, raw_target_files
    )

    targets = list(
      filter(lambda x: dep_graph.nodes[x]["is_target"], dep_graph.nodes)
    )

    print(
      *list(x + ": " + str(dep_graph.nodes[x]["props"]) for x in targets),
      sep="\n"
    )


def main(files: tp.List[Path]) -> None:
    for file in files:
        _solve(file)
