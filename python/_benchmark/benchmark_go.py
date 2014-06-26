

import os
import time
import itertools
import subprocess


# path = 'C:\\studio'
path = 'C:\\'
os.chdir(path)

queries = ('.Shot', '.Asset', '.Version', '.Project', '#MyBen')

runs = list()  # Number of runs
max_runs = 3
max_count = 1

items = 0
for root, _, _ in os.walk(path):
    items += 1

print "Scanning a hierarchy of {} items".format(items)

for run in range(max_runs):
    count = 0
    matches = 0
    clock = time.clock()

    for query in itertools.cycle(queries):
        proc = subprocess.Popen(['gocq', query],
                                stdout=subprocess.PIPE,
                                shell=True)
        matches += len(proc.stdout.readlines())

        count += 1
        if count > max_count - 1:
            break

    time_taken = time.clock() - clock
    runs.append(time_taken)

    print "%i queries, %i matches in %f seconds" % (count,
                                                    matches,
                                                    time_taken)
average = (sum(runs) / max_runs) / max_count
print "  Average time/query: %f seconds" % average

# Results:

# Scanning a hierarchy of 3601 items
# 1 queries, 7 matches in 1.425702 seconds
# 1 queries, 7 matches in 1.420373 seconds
# 1 queries, 7 matches in 1.419541 seconds
#   Average time/query: 1.421872 seconds

# Scanning a hierarchy of 47715 items
# 1 queries, 14 matches in 18.015012 seconds
# 1 queries, 14 matches in 17.951607 seconds
# 1 queries, 14 matches in 17.994924 seconds
#   Average time/query: 17.987181 seconds
