import json
import os.path
import operator
from collections import defaultdict
# import mdp
import numpy as np
import pandas as p
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import gng
from random import randrange


cutoff = 9

def parse_json(selection=['Pittsburgh']):
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
  for ind, user in enumerate(user_reviews.keys()):
    if len(user_reviews[user].keys()) > cutoff:
      users['user_'+str(ind)] = user_reviews[user]

  print("Users after cutoff: " + str(len(users.keys())))

  with open('data/users.json', 'w') as outfile:
    json.dump(users, outfile)

  ######################## END PARSE ########

# def main():

if not os.path.isfile('data/users.json'):
  parse_json(['Pittsburgh'])

for line in open('data/businesses.json'):
  # only one line
  businesses = json.loads(line)
  # business[business_id] = review_count
print("Businesses: " + str(len(businesses)))

for line in open('data/users.json'):
  # only one line
  users = json.loads(line)
  # users[user_id][business_id] = rating

print("Users: " + str(len(users)))

df = p.DataFrame(users).T.fillna(0)

def getUser():
  return df.values[randrange(len(df))]

# plt.figure()
# plt.plot(df.values)
s = input("waiting: ")

gng = gng.GrowingNeuralGas(getUser, 1338, verbose=0)
for i in range(15000):
  gng.step()
  if gng.stepCount % 1000==0:
    print gng


  # gng = mdp.nodes.GrowingNeuralGasNode(max_nodes=75)
  # STEP = 500

  # for i in range(0,x.shape[0],STEP):
  #   gng.train(x[i:i+STEP])
  #   # [...] plotting instructions

  # gng.stop_training()



# main()





