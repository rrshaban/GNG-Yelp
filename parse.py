import json
import os.path
import operator
from collections import defaultdict

cutoff = 9

def parse(selection=['Pittsburgh']):
  businesses = list()
  for line in open('data/yelp_academic_dataset_business.json'):
    businesses.append(json.loads(line))

  selection = ['Pittsburgh']
  sel_businesses = dict()
  for bus in businesses:
    if (bus['city'] in selection) and (bus['review_count'] > cutoff):
      sel_businesses[bus['business_id']] = bus['review_count']

  print("Businesses: " + str(len(sel_businesses.keys())))

  with open('data/businesses.json', 'w') as outfile:
    json.dump(sel_businesses, outfile)

  user_reviews = defaultdict(dict)
  for line in open('data/yelp_academic_dataset_review.json'):
    l = json.loads(line)
    
    if l['business_id'] in sel_businesses:
      user_reviews[l['user_id']][l['business_id']] = l['stars']

  print("Users: " + str(len(user_reviews.keys())))

  with open('data/user_reviews.json', 'w') as outfile:
    json.dump(user_reviews, outfile)

  users = defaultdict(dict)
  for user in user_reviews.keys():
    if len(user_reviews[user].keys()) > cutoff:
      users[user] = user_reviews[user]

  print("Users after cutoff: " + str(len(users.keys())))

  with open('data/users.json', 'w') as outfile:
    json.dump(users, outfile)

if not os.path.isfile('data/users.json'):
  parse()

def main():

  for line in open('data/businesses.json'):
    # only one line
    businesses = json.loads(line)
    # business[business_id] = review_count

  for line in open('data/users.json'):
    # only one line
    users = json.loads(line)
    # users[user_id][business_id] = rating

  print("Businesses: " + str(len(businesses)))
  print("Users: " + str(len(users)))


