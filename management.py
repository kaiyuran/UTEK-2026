from collections import defaultdict, deque
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass


@dataclass
class Object:
    """Simple container for an object/drone: id, priority, start/end nodes and candidate paths."""
    id: int
    priority: int  # Higher number = higher priority
    start_node: int
    end_node: int
    paths: List[List[int]]  # Top three paths (paths[0] is most optimal)


class CollisionAvoidanceScheduler:
    
    def __init__(self, tree: Dict[int, List[int]], velocity: float = 1.0):
        """Create a scheduler for the given adjacency `tree` and travel `velocity` (time per edge)."""
        self.tree = tree
        self.velocity = float(velocity)
        self.eps = 1e-6

    def _get_node_timeline(self, path: List[int], start_time: float = 0.0) -> Dict[int, List[float]]:
        """Return a mapping node -> list of visit times when following `path` starting at `start_time`.
        Time increases by `self.velocity` per edge."""
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
        """Detect collisions in `schedules`.
        schedules: mapping object_id -> (path, start_time).
        Returns list of tuples (obj1_id, obj2_id, node, collision_time)."""
        collisions: List[Tuple[int, int, int, float]] = []
        object_timelines: Dict[int, Dict[int, List[float]]] = {}
        # Build a timeline for each object: node -> list of times the object is at that node
        for obj_id, (path, start_time) in schedules.items():
            object_timelines[obj_id] = self._get_node_timeline(path, start_time)
        object_ids = list(schedules.keys())
        # Compare every pair of objects to find overlapping visits to the same node
        for i in range(len(object_ids)):
            for j in range(i + 1, len(object_ids)):
                obj1_id = object_ids[i]
                obj2_id = object_ids[j]
                timeline1 = object_timelines.get(obj1_id, {})
                timeline2 = object_timelines.get(obj2_id, {})
                # Only consider nodes both objects visit
                common_nodes = set(timeline1.keys()) & set(timeline2.keys())
                for node in common_nodes:
                    # Compare all visit times for the shared node
                    for t1 in timeline1[node]:
                        for t2 in timeline2[node]:
                            # If both are at the node at (nearly) the same time, record a collision
                            if abs(t1 - t2) <= self.eps:
                                # Use the average of the two times as the collision timestamp
                                collisions.append((obj1_id, obj2_id, node, (t1 + t2) / 2.0))
        return collisions

    def _has_collisions(self, schedules: Dict[int, Tuple[List[int], float]]) -> bool:
        """Return True if any collision exists in `schedules`."""
        return len(self._find_collisions(schedules)) > 0

    def schedule(self, objects: List[Object], max_iterations: int = 100) -> Dict[int, Tuple[List[int], float]]:
        """Compute a collision-free schedule for given `objects`.
        Iteratively tries alternative paths and/or delays to remove collisions.
        Returns mapping object_id -> (chosen_path, start_time)."""
        # Sort by priority (higher first), break ties using id
        sorted_objects = sorted(objects, key=lambda x: (x.priority, -x.id), reverse=True)
        schedules: Dict[int, Tuple[List[int], float]] = {}
        # Initialize each object on its best path and starting at time 0.0
        for obj in sorted_objects:
            schedules[obj.id] = (obj.paths[0], 0.0)
        iteration = 0
        # Iteratively resolve collisions until none remain or hit iteration limit
        while iteration < max_iterations:
            iteration += 1
            collisions = self._find_collisions(schedules)
            if not collisions:
                break
            # adjustments maps object_id -> list of collision tuples where this object should yield
            adjustments: Dict[int, List[Tuple[int, int, float]]] = {}
            for obj1_id, obj2_id, node, time in collisions:
                # Identify the two objects and decide which should yield (by priority or tie-breaker)
                obj1 = next((o for o in objects if o.id == obj1_id), None)
                obj2 = next((o for o in objects if o.id == obj2_id), None)
                if obj1 is None or obj2 is None:
                    continue
                if obj1.priority < obj2.priority:
                    lower_id = obj1_id
                elif obj2.priority < obj1.priority:
                    lower_id = obj2_id
                else:
                    # Tie-break: the larger id yields (arbritrary but consistent)
                    lower_id = max(obj1_id, obj2_id)
                adjustments.setdefault(lower_id, []).append((obj1_id, obj2_id, time))
            # Apply yielding behaviour: try an alternate path first, otherwise delay start time
            for lower_id in sorted(adjustments.keys(), key=lambda oid: (next(o.priority for o in objects if o.id == oid), oid)):
                lower_obj = next((o for o in objects if o.id == lower_id), None)
                if lower_obj is None:
                    continue
                current_path, current_start = schedules[lower_id]
                # If there is another candidate path, switch to it to avoid collision without delaying
                current_index = lower_obj.paths.index(current_path) if current_path in lower_obj.paths else 0
                if current_index < len(lower_obj.paths) - 1:
                    schedules[lower_id] = (lower_obj.paths[current_index + 1], current_start)
                else:
                    # No alternate path available: delay the object's start time by one edge time
                    schedules[lower_id] = (current_path, current_start + self.velocity)
            # If we've been iterating for a while, also attempt small half-step delays to break stubborn collisions
            if iteration > max_iterations // 2:
                collisions = self._find_collisions(schedules)
                if collisions:
                    for obj1_id, obj2_id, node, time in collisions:
                        obj1 = next((o for o in objects if o.id == obj1_id), None)
                        obj2 = next((o for o in objects if o.id == obj2_id), None)
                        if obj1 and obj2:
                            if obj1.priority < obj2.priority:
                                p, s = schedules[obj1_id]
                                # Small half-step delay to try to resolve remaining collisions
                                schedules[obj1_id] = (p, s + self.velocity * 0.5)
                            else:
                                p, s = schedules[obj2_id]
                                schedules[obj2_id] = (p, s + self.velocity * 0.5)
        return schedules


# `schedules` returned by `CollisionAvoidanceScheduler.schedule` is a dict mapping object_id -> (chosen_path, start_time).
# Example printed output:
# { 1: ([0, 2, 3], 0.0), 2: ([1, 4, 5], 1.0) }
# - key: object id (int)
# - value: tuple(path: List[int], start_time: float)
# Where `path` is the selected node sequence and `start_time` is when the object is at the first node.
# Printing `schedules` will show object ids as keys and the chosen path plus start time as the tuple value.
    