import heapq
hpush=heapq.heappush
hpop=heapq.heappop

import random
from collections import Counter

def simulate(beta, pop, reportTimes=None, seed=1048):
    # returns [trans, orbit]
    if seed is not None:
        random.seed(seed)

    C = 0; I = 0
    queue = []
    tie = 0
    def push(t, ev):
        # tie-breaker avoids dict compare on equal times
        nonlocal tie
        hpush(queue, (t, tie, ev)); tie += 1

    trans = [{}]  # index-0 unseen
    orbit = []
    last_time = 0.0

    ridx = 0

    push(0.0, {"type":"contact","primary":0,"filter":pop})

    while queue:
        time, _, event = hpop(queue)
        last_time = time

        # record all report times passed by this event
        if reportTimes is not None:
            while ridx < len(reportTimes) and time >= reportTimes[ridx]:
                orbit.append({"t":reportTimes[ridx],"C":C,"I":I})
                ridx += 1

        match event["type"]:
            case "contact":
                primary = event["primary"]
                S = pop - C
                # thin by S_fire / S_start
                if S > 0 and random.random() < S / event["filter"]:
                    # new infector
                    C += 1; I += 1
                    trans.append({"in":time,"out":[]})
                    if primary > 0:
                        trans[primary]["out"].append(time)

                    # proposals for new infector
                    filter = S
                    Re = beta * filter / pop
                    pInf = Re / (Re + 1)
                    delta = 1 / (Re + 1)

                    next = "contact" if random.random() < pInf else "recover"
                    t_event = time + delta * random.expovariate(1)

                    while next == "contact":
                        push(t_event, {"type":"contact","primary":C,"filter":filter})
                        next = "contact" if random.random() < pInf else "recover"
                        t_event += delta * random.expovariate(1)

                    # recovery
                    push(t_event, {"type":"recover","focus":C})
                    trans[C]["recover"] = t_event

            case "recover":
                I -= 1

    # always record final state at exact last_time
    orbit.append({"t":last_time,"C":C,"I":I})
    return [trans, orbit]


def offspring_counts(trans):
    # histogram of out-degree
    counts = Counter()
    if trans and trans[0] == {}:
        trans = trans[1:]
    for infector in trans:
        k = len(infector.get("out", []))
        counts[k] += 1
    return counts

