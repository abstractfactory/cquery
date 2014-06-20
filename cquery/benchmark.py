from __future__ import absolute_import

import os
import time
import itertools
import cquery

path = r'C:\studio\content\jobs\spiderman'
os.chdir(path)

queries = ('.Shot', '.Asset', '.Version', '.Project', '#MyBen')

runs = list()
max_runs = 10
max_count = 100

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

# Test results
# 10 queries, 38 matches in 0.132298 seconds
# 10 queries, 38 matches in 0.130776 seconds
# 10 queries, 38 matches in 0.130859 seconds
#   Average time/query: 0.013131s
#
# 100 queries, 380 matches in 1.175440 seconds
# 100 queries, 380 matches in 1.165187 seconds
# 100 queries, 380 matches in 1.162648 seconds
# 100 queries, 380 matches in 1.168100 seconds
# 100 queries, 380 matches in 1.165442 seconds
# 100 queries, 380 matches in 1.170666 seconds
# 100 queries, 380 matches in 1.160844 seconds
# 100 queries, 380 matches in 1.164311 seconds
# 100 queries, 380 matches in 1.159229 seconds
# 100 queries, 380 matches in 1.169779 seconds
#   Average time/query: 0.011662 seconds
