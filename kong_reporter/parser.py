import sys
import time
import datetime

sizes = {}
hits = {}

for line in sys.stdin:
    if 'q' == line.rstrip():
        break
    l = line.split(" ")
    if len(l) > 9  and l[5] == '"GET':
        a = datetime.datetime.strptime(l[3], '[%d/%b/%Y:%H:%M:%S')
        if(datetime.datetime.now() - a < datetime.timedelta(days=30)):
            prevSize = sizes.get(l[6].split("?")[0],0)
            prevHits = hits.get(l[6].split("?")[0],0)
            sizes[l[6].split("?")[0]] = prevSize + int(l[9])
            hits[l[6].split("?")[0]] = prevHits + 1
print("<h1>Kong Log Report for last 30 days</h1>")
print("<h2> Sizes per Endpoint </h2>")
print(sizes)
print("<h2> Hits per Endpoint </h2>")
print(hits)
