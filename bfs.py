from typing import Dict, List


def bfs(adj: Dict[int, List[int]], start: int, end: int, paths_needed: int) -> List[List[int]]:
    """Return up to `paths_needed` simple paths from start to end using BFS expansion."""

    curr_paths: List[List[int]] = [[start]]
    final_paths: List[List[int]] = []

    while True:
        new_paths: List[List[int]] = []
        for path in curr_paths:
            last = path[-1]
            for node in adj.get(last, []):
                if node == end:
                    final_paths.append(path + [node])
                elif node not in path:
                    new_paths.append(path + [node])

        if len(final_paths) >= paths_needed or not new_paths:
            break

        curr_paths = new_paths

    if len(final_paths) > paths_needed:
        return final_paths[:paths_needed]

    return final_paths