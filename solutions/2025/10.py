from typing import Any
import itertools
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def parse_line(line):
    indicators, rem = line.split("] ")
    indicators = indicators.replace("[","")
    indicators = [i == "#" for i in indicators]
    wiring_schematics, rem = rem.split(" {")
    wiring_schematics = list(map(eval,wiring_schematics.split(" ")))
    joltages = eval("[" + rem.replace("}","]"))
    return indicators, wiring_schematics, joltages



def apply_presses(state, wiring_schematics, press_counts):
    num_presses = 0
    for wiring_schematic,count in zip(wiring_schematics,press_counts):
        if count == 0:
            continue
        num_presses += 1
        if isinstance(wiring_schematic,int):
            wiring_schematic = [wiring_schematic]
        for wire in wiring_schematic:
            state[wire] = not state[wire]
    return state, num_presses

def a(input: str) -> Any:
    # press a button at most two times, try all combinations and store attlempts
    entries = [parse_line(line) for line in input.splitlines()]
    counts = []
    for indicators, wiring_schematics, _ in entries:
        min_count = None
        for press_counts in itertools.product([0,1], repeat=len(wiring_schematics)):
            state, num_presses = apply_presses([False]*len(indicators), wiring_schematics, press_counts)
            if state == indicators:
                if min_count is None:
                    min_count = num_presses
                else:
                    min_count = min(min_count, num_presses)
        counts.append(min_count)
    return sum(counts)


def apply_presses_joltage(state, wiring_schematics, press_counts, desired_state):
    num_presses = 0
    for wiring_schematic,count in zip(wiring_schematics,press_counts):
        num_presses += count
        if isinstance(wiring_schematic,int):
            wiring_schematic = [wiring_schematic]
        for wire in wiring_schematic:
            state[wire] += count
        
    return state, num_presses

import pulp
import numpy as np

def _solve_entry(entry):
    _, wiring_schematics, target = entry

    target = np.array(target)
    n_buttons = len(wiring_schematics)
    n_jolts = len(target)

    # Build M matrix
    M = np.zeros((n_buttons, n_jolts), dtype=int)
    for i, w in enumerate(wiring_schematics):
        if isinstance(w, int):
            w = [w]
        for j in w:
            M[i, j] = 1

    prob = pulp.LpProblem("ButtonPresses", pulp.LpMinimize)

    pc = [
        pulp.LpVariable(f"pc_{i}", lowBound=0, cat="Integer")
        for i in range(n_buttons)
    ]

    prob += pulp.lpSum(pc)

    for j in range(n_jolts):
        prob += pulp.lpSum(pc[i] * M[i, j] for i in range(n_buttons)) == target[j]

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        return None

    # Return sum of presses


def b(input: str):
    entries = [parse_line(line) for line in input.splitlines()]

    n_workers = cpu_count()

    counts = []
    with Pool(n_workers) as pool:
        for result in tqdm(pool.imap_unordered(_solve_entry, entries),
                           total=len(entries),
                           desc="Processing entries"):
            counts.append(result)

    return int(sum(counts))