import sys
import time
import datetime

sizes = {}
hits = {}

for line in sys.stdin:
  try:
    if 'q' == line.rstrip():
      break
    l = line.split(" ")
    if len(l) > 9 and l[5] == '"GET':
      a = datetime.datetime.strptime(l[3], '[%d/%b/%Y:%H:%M:%S')
      if (datetime.datetime.now() - a < datetime.timedelta(days = 30)):
        prevSize = sizes.get(l[6].split("?")[0], 0)
        prevHits = hits.get(l[6].split("?")[0], 0)
        sizes[l[6].split("?")[0]] = prevSize + int(l[9])
        hits[l[6].split("?")[0]] = prevHits + 1
  except:
    print("error on a line")

print("*Kong Log Report for last 30 days*")
print("Total bytes sent to client per Endpoint:")
print(sizes)
print("\n")
print("Total hits per Endpoint:")
print(hits)
