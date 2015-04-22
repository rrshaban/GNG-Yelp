import json
import operator

b = list()
for line in open('data/yelp_academic_dataset_business.json'):
  b.append(json.loads(line))

c = dict()
for bus in b:
  if bus['city'] in c:
    c[bus['city']] += 1
  else:
    c[bus['city']] = 1
sorted_c = sorted(c.items(), key=operator.itemgetter(1), reverse=True)

print(sorted_c[:20])