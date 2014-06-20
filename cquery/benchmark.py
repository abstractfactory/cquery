from __future__ import absolute_import

import os
import time
import itertools
import cquery

path = r'C:\studio\content\jobs\spiderman'
os.chdir(path)

queries = ('.Shot', '.Asset', '.Version', '.Project', '#MyBen')

runs = list()
max_runs = 3
max_count = 10

for run in range(max_runs):
    count = 0
    matches = 0
    clock = time.clock()

    for query in itertools.cycle(queries):
        matches += len(cquery.cquery(query=query, silent=True))

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
