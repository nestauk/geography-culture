import sys
import datetime

for line in sys.stdin:
    try:
        print datetime.datetime.fromtimestamp(int(line)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        print line.rstrip("\n")
