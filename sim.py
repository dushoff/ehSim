import heapq
hpush=heapq.heappush
hpop=heapq.heappop

import random
random.seed(1051)

from collections import Counter

pop = 1e5
beta = 5

## Not using I for anything, maybe don't keep track
C = 0; I = 0

queue = []

## Add a blank for the zero-th (unseen) transmitter for now
## We could def think of things to add here, including the possibility of more than one initial infection
trans = [{}]
hpush (queue, (0, 
	{"type": "contact"
		,"primary": 0
		, "filter": pop
	}
))

while queue:
	time, event = hpop(queue)
	match event['type']:
		case "contact":
			## Is “target” still susceptible?
			S = pop-C
			if random.random() < S/event['filter']:
				C += 1; I += 1

				## Create new infector and pre-calculate all of their events
				trans.append({"in": time, "out": []})
				Re = beta*S/pop; pInf = Re/(Re+1); delta = 1/(Re+1)
				next = "contact" if random.random() < pInf else "recover"
				time += delta*random.expovariate(1)
				while (next == "contact"):
					hpush (queue, (time, 
						{"type": "contact"
							,"primary": C
							, "filter": S
						}
					))
					trans[C]["out"].append(time)
					next = "contact" if random.random() < pInf else "recover"
					time += delta*random.expovariate(1)
				hpush (queue, (time, 
					{"type": "recover" ,"focus": event['primary']}
				))
				trans[C]["recover"] = time
			## else failed contact, do nothing

		case "recover":
			I -= 1
	## end match
## end while

counts = Counter()
trans.pop(0)
for infector in trans:
	counts[len(infector["out"])] += 1

print(counts)
