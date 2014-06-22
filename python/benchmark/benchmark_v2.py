from __future__ import absolute_import

import os
import time
import itertools

import cquery_v2 as cquery


# path = 'C:\\studio'
path = 'C:\\'
os.chdir(path)

selectors = ('.Shot', '.Asset', '.Version', '.Project', '#MyBen')

runs = list()
max_runs = 3
max_queries = 1

items = 0
for root, _, _ in os.walk(path):
    items += 1

print "Scanning a hierarchy of {} items".format(items)

for run in range(max_runs):
    queries = 0
    matches = 0
    clock = time.clock()

    for selector in itertools.cycle(selectors):
        matches += len(cquery.cquery(selector=selector))

        queries += 1
        if queries > max_queries - 1:
            break

    time_taken = time.clock() - clock
    runs.append(time_taken)

    print "%i queries, %i matches in %f seconds" % (max_queries,
                                                    matches,
                                                    time_taken)
average = (sum(runs) / max_runs) / max_queries
print "  Average time/query: %f seconds" % average

# Test results

# Scanning a hierarchy of 3601 items
# 1 queries, 7 matches in 1.494072 seconds
# 1 queries, 7 matches in 1.480471 seconds
# 1 queries, 7 matches in 1.477589 seconds
#   Average time/query: 1.484044 seconds

# Scanning a hierarchy of 47715 items
# 1 queries, 14 matches in 19.888399 seconds
# 1 queries, 14 matches in 20.078811 seconds
# 1 queries, 14 matches in 19.879660 seconds
#   Average time/query: 19.948957 seconds
