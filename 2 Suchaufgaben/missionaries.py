from __future__ import annotations
from typing import List, Optional
from generic_search import bfs, Node, node_to_path

MAX_NUM: int = 3


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries  # Missionare am Westufer
        self.wc: int = cannibals  # Kannibalen am Westufer
        self.em: int = MAX_NUM - self.wm  # Missionare am Ostufer
        self.ec: int = MAX_NUM - self.wc  # Cannibalen am Ostufer
        self.boat: bool = boat  # Boot am Westufer oder nicht

    def __str__(self) -> str:
        return ("Am Westufer sind {} Missionare und {} Kannibalen.\n"
                "Am Ostufer sind {} Missionare und {} Kannibalen\n"
                "Das Boot ist am {}ufer.") \
            .format(self.wm, self.wc, self.em, self.ec, ("West" if self.boat else "Ost"))

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return True
        return True

    def successors(self) -> List[MCState]:
        sucs: List[MCState] = []
        if self.boat:  # Boot am Westufer
            if self.wm > 1:
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:  # Boot am Ostufer
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.ec > 0) and (self.em > 0):
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))
        return [x for x in sucs if x.is_legal]


def display_solution(path: List[MCState]):
    if len(path) == 0:  # Gültigkeitsprüfung
        return
    old_state: MCState = path[0]
    print(old_state)
    for current_state in path[1:]:
        if current_state.boat:
            print("{} Missionare und {} Kanibalen vom Ostufer zum Westufe transportiert.\n"
                  .format(old_state.em - current_state.em,
                          old_state.ec - current_state.ec))
        else:
            print("{} Missionare und {} Kannibalen vom Westufer zum Ostufer transportiert.\n"
                  .format(old_state.wm - current_state.wm,
                          old_state.wc - current_state.wc))
        print(current_state)
        old_state = current_state


if __name__ == "__main__":
    start: MCState = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(start, MCState.goal_test, MCState.successors)
    if solution is None:
        print("Keine Lösung gefunden!")
    else:
        path: List[MCState] = node_to_path(solution)
        display_solution(path)
