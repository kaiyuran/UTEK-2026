from typing import List, Dict, Any, Tuple

from bfs import bfs
from management import CollisionAvoidanceScheduler, Object


class Calculations:

    def __init__(self, tree: Dict[int, List[int]], paths_needed: int = 3, velocity: float = 1.0):
        self.tree = tree
        self.paths_needed = max(1, int(paths_needed))
        self.scheduler = CollisionAvoidanceScheduler(tree, velocity)

    def build_objects(self, objects_info: List[Dict[str, Any]]) -> List[Object]:
        objects: List[Object] = []

        for info in objects_info:
            obj_id = info.get("id")
            start = info.get("start_node") if "start_node" in info else info.get("start")
            end = info.get("end_node") if "end_node" in info else info.get("end")
            priority = int(info.get("priority", 0))

            paths = bfs(self.tree, start, end, self.paths_needed)

            objects.append(Object(id=int(obj_id), priority=priority, start_node=int(start), end_node=int(end), paths=paths))

        return objects

    def schedule(self, objects_info: List[Dict[str, Any]]) -> Dict[int, Tuple[List[int], float]]:
        objs = self.build_objects(objects_info)
        return self.scheduler.schedule(objs)



