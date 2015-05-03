import json
import os.path
import operator
from collections import defaultdict
# import mdp
import numpy as np
import pandas as p
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
import gng as g
from random import randrange


cutoff = 9

def parse_json(selection=['Pittsburgh']):
  businesses = list()
  for line in open('data/yelp_academic_dataset_business.json'):
    businesses.append(json.loads(line))

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
      users[user] = user_reviews[user]

  print("Users after cutoff: " + str(len(users.keys())))

  with open('data/users.json', 'w') as outfile:
    json.dump(users, outfile)

  ######################## END PARSE ########

def get_user_id(users_dict):

  while True:
    s = raw_input("Input user ID or 'q' to exit: ")

    if s == 'q':
      quit()

    if s in users_dict:
      return s
    else:
      print "User ID was not found, please try again."


def main():

  sel = ['Pittsburgh']

  print("Loading user and restaurant data...")

  if not os.path.isfile('data/users.json'):
    print("User data not pre-parsed -- will now parse\n")
    parse_json(sel)
    print("User data parsing finised!\n")

  for line in open('data/businesses.json'):
    # only one line
    businesses = json.loads(line)
    # business[business_id] = review_count

  print("Restaurants: " + str(len(businesses)))

  for line in open('data/users.json'):
    # only one line
    users = json.loads(line)
    # users[user_id][business_id] = rating

  print("Users: " + str(len(users)))

  df = p.DataFrame(data=users).T.fillna(0) # fill in missing values with 0

  def get_random_user():
    u = df.iloc[randrange(len(df))]
    return (u.values, u.name)

  print("Building GNG network...")

  gng = g.GrowingNeuralGas(get_random_user, 1338, verbose=0)
  for i in range(100): # 6000
    gng.step()
    if gng.stepCount % 100==0:
      print gng


  print("Recommendation system ready!")

  user_id = get_user_id(users)
  user_node = df.loc[user_id].values

  rec_users = [x.getUser() for x in gng.computeDistances(user_node)]

  res = dict()
  for user in rec_users:
    res.update(users[user])
    print "We recommend you follow the following users: ", user

  sorted_res = sorted(res.items(), key=operator.itemgetter(1), reverse=True)

  print "\nWe recommend you look at the following restaurants: "
  for res_id, rating in sorted_res[:5]:
    print res_id, " with a rating of ", rating






  # print type(node)
  # print type(df.values[randrange(len(df))])

  # -0itF0VWVBe3k2AdfUReGA


if __name__ == '__main__':
  main()





