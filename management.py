from collections import defaultdict, deque
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass


@dataclass
class Object:
    id: int
    priority: int  # Higher number = higher priority
    start_node: int
    end_node: int
    paths: List[List[int]]  # Top three paths (paths[0] is most optimal)


class CollisionAvoidanceScheduler:
    """Simplified scheduler: deterministic resolution, no raised exceptions for invalid inputs or unresolved collisions."""
    def __init__(self, tree: Dict[int, List[int]], velocity: float = 1.0):
        self.tree = tree
        self.velocity = float(velocity)
        self.eps = 1e-6

    def _get_node_timeline(self, path: List[int], start_time: float = 0.0) -> Dict[int, List[float]]:
        from collections import defaultdict
        timeline: Dict[int, List[float]] = defaultdict(list)
        current_time = float(start_time)
        if not path:
            return {}
        timeline[path[0]].append(current_time)
        for i in range(len(path) - 1):
            current_time += self.velocity
            timeline[path[i + 1]].append(current_time)
        return timeline

    def _find_collisions(self, schedules: Dict[int, Tuple[List[int], float]]) -> List[Tuple[int, int, int, float]]:
        collisions: List[Tuple[int, int, int, float]] = []
        object_timelines: Dict[int, Dict[int, List[float]]] = {}
        for obj_id, (path, start_time) in schedules.items():
            object_timelines[obj_id] = self._get_node_timeline(path, start_time)
        object_ids = list(schedules.keys())
        for i in range(len(object_ids)):
            for j in range(i + 1, len(object_ids)):
                obj1_id = object_ids[i]
                obj2_id = object_ids[j]
                timeline1 = object_timelines.get(obj1_id, {})
                timeline2 = object_timelines.get(obj2_id, {})
                common_nodes = set(timeline1.keys()) & set(timeline2.keys())
                for node in common_nodes:
                    for t1 in timeline1[node]:
                        for t2 in timeline2[node]:
                            if abs(t1 - t2) <= self.eps:
                                collisions.append((obj1_id, obj2_id, node, (t1 + t2) / 2.0))
        return collisions

    def _has_collisions(self, schedules: Dict[int, Tuple[List[int], float]]) -> bool:
        return len(self._find_collisions(schedules)) > 0

    def schedule(self, objects: List[Object], max_iterations: int = 100) -> Dict[int, Tuple[List[int], float]]:
        sorted_objects = sorted(objects, key=lambda x: (x.priority, -x.id), reverse=True)
        schedules: Dict[int, Tuple[List[int], float]] = {}
        for obj in sorted_objects:
            schedules[obj.id] = (obj.paths[0], 0.0)
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            collisions = self._find_collisions(schedules)
            if not collisions:
                break
            adjustments: Dict[int, List[Tuple[int, int, float]]] = {}
            for obj1_id, obj2_id, node, time in collisions:
                obj1 = next((o for o in objects if o.id == obj1_id), None)
                obj2 = next((o for o in objects if o.id == obj2_id), None)
                if obj1 is None or obj2 is None:
                    continue
                if obj1.priority < obj2.priority:
                    lower_id = obj1_id
                elif obj2.priority < obj1.priority:
                    lower_id = obj2_id
                else:
                    lower_id = max(obj1_id, obj2_id)
                adjustments.setdefault(lower_id, []).append((obj1_id, obj2_id, time))
            for lower_id in sorted(adjustments.keys(), key=lambda oid: (next(o.priority for o in objects if o.id == oid), oid)):
                lower_obj = next((o for o in objects if o.id == lower_id), None)
                if lower_obj is None:
                    continue
                current_path, current_start = schedules[lower_id]
                current_index = lower_obj.paths.index(current_path) if current_path in lower_obj.paths else 0
                if current_index < len(lower_obj.paths) - 1:
                    schedules[lower_id] = (lower_obj.paths[current_index + 1], current_start)
                else:
                    schedules[lower_id] = (current_path, current_start + self.velocity)
            if iteration > max_iterations // 2:
                collisions = self._find_collisions(schedules)
                if collisions:
                    for obj1_id, obj2_id, node, time in collisions:
                        obj1 = next((o for o in objects if o.id == obj1_id), None)
                        obj2 = next((o for o in objects if o.id == obj2_id), None)
                        if obj1 and obj2:
                            if obj1.priority < obj2.priority:
                                p, s = schedules[obj1_id]
                                schedules[obj1_id] = (p, s + self.velocity * 0.5)
                            else:
                                p, s = schedules[obj2_id]
                                schedules[obj2_id] = (p, s + self.velocity * 0.5)
        return schedules
    
    