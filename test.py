from simfuns import simulate, offspring_counts

# no reporting
trans, orbit = simulate(beta=3, pop=int(1e5), reportTimes=None)
counts = offspring_counts(trans)
print(counts)

# report at t=10, 20, 30, then stop after t=30
trans, orbit = simulate(beta=3, pop=int(1e5), reportTimes=[10,20,30])
print(orbit)

# "infinite" horizon (report only once at a huge time)
trans, orbit = simulate(beta=3, pop=int(1e5), reportTimes=None)
print(orbit) 

