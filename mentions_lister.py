import sys
from authentication import getSession
import urllib.parse
import json
import akari

org_ids = sys.argv

session = getSession()

#api_path = 'https://api.twitter.com/1.1/search/tweets.json'
#query_param = '?q=' + urllib.parse.quote('to:Akari1288+since:2019-01-25') + '&count=100&src=typd'
#
#user_ids = []
#while len(query_param) > 0:
#  req = session.get(api_path + query_param)
#  res = json.loads(req.text)
#  statuses = res['statuses']
#
#  for status in statuses:
#    if status['in_reply_to_status_id_str'] in org_ids[1:len(org_ids)]:
#      id_str = status['user']['id_str']
#      screen_name = status['user']['screen_name']
#      if (screen_name != 'Akari1288') and not(id_str in user_ids):
#        user_ids.append(id_str)
#
#  try:
#    query_param = res['search_metadata']['next_results']
#  except KeyError:
#    query_param = ''

api_path = 'https://api.twitter.com/1.1/tweets/search/30day/st30days.json'
params = {
  "query" : '@Akari1288',
  "maxResults" : 100,
  "fromDate" : '201901250000',
  "toDate" : '201902160000'
}

user_ids = []
next = 'next'
while len(next) > 0:
  req = session.get(api_path, params = params)
  res = json.loads(req.text)
  statuses = []
  try:
    statuses = res['results']
  except KeyError:
    statuses = []

  for status in statuses:
    if status['in_reply_to_status_id_str'] in org_ids[1:len(org_ids)]:
      id_str = status['user']['id_str']
      screen_name = status['user']['screen_name']
      if (screen_name != 'Akari1288') and not(id_str in user_ids):
        user_ids.append(id_str)

  try:
    next = res['next']
    params['next'] = next
  except KeyError:
    next = ''

lists = akari.allocate(session, user_ids)

with open('./mention_normal.txt', mode='w', encoding='utf-8') as f:
  print('---------- normal')
  for user in lists['normal']:
    line = user['name'] + ', @' + user['screen_name']
    print(line)
    f.write(line)
    f.write('\n')

with open('./mention_retweeter.txt', mode='w', encoding='utf-8') as f:
  print('---------- retweeter')
  for user in lists['retweeter']:
    line = user['name'] + ', @' + user['screen_name']
    print(line)
    f.write(line)
    f.write('\n')

with open('./mention_abnormal.txt', mode='w', encoding='utf-8') as f:
  print('---------- abnormal')
  for user in lists['abnormal']:
    line = user['name'] + ', @' + user['screen_name']
    print(line)
    f.write(line)
    f.write('\n')
