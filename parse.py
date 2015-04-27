import json
import operator
from collections import defaultdict

cutoff = 9


businesses = list()
for line in open('data/yelp_academic_dataset_business.json'):
  businesses.append(json.loads(line))

selection = ['Pittsburgh']
sel_businesses = dict()
for bus in businesses:
  if (bus['city'] in selection) and (bus['review_count'] > cutoff):
    sel_businesses[bus['business_id']] = bus['review_count']

print("Businesses: " + str(len(sel_businesses.keys())))

user_reviews = defaultdict(dict)
for line in open('data/yelp_academic_dataset_review.json'):
  l = json.loads(line)
  
  if l['business_id'] in sel_businesses:
    user_reviews[l['user_id']][l['business_id']] = l['stars']

print("Users: " + str(len(user_reviews.keys())))

users = defaultdict(dict)
for user in user_reviews.keys():
  if len(user_reviews[user].keys()) > cutoff:
    users[user] = user_reviews[user]


print(users[users.keys().first])