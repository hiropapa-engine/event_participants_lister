import json
import sys
import time

def allocate(session, user_ids):

  lists = {
    'normal' : [],
    'retweeter' : [],
    'abnormal' : []
  }

  ite = getSliceIterator(user_ids)
  for slice in ite:
    api_path = 'https://api.twitter.com/1.1/users/lookup.json'
    params = {
      'user_id' : ','.join(slice)
    }
    req = session.get(api_path, params = params)
    res = json.loads(req.text)
    for user in res:
      tl_api_path = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
      tl_params = {
        'user_id' : user['id_str'],
        'count' : 5,
        'include_rts' : True
      }
      tl_req = None
      tl_res = None
      status_code = 0

      while True:
        tl_req = session.get(tl_api_path, params = tl_params)
        tl_res = json.loads(tl_req.text)
        status_code = tl_req.status_code

        # ステータスコード429(Rate limit exceeded)の場合、10分待ってから再実行
        if status_code == 200:
          print(user['screen_name'] + " : OK.")
          break
        elif status_code == 429:
          print(user['screen_name'] + " : Waiting.")
          time.sleep(60)
        else:
          print(user['screen_name'] + " : Error.")
          print(tl_res)
          sys.exit()

      x = 5 if len(tl_res) > 5 else len(tl_res)
      retweeter = True
      for i in range(0, x):
        if 'retweeted_status' in tl_res[i].keys():
          continue
        else:
          retweeter = False
          break;

      if retweeter == True:
        lists['retweeter'].append(user)
        continue;

      if len(user['profile_image_url']) > 0:
        lists['normal'].append(user)
        continue

      if len(user['description']) > 0:
        lists['normal'].append(user)
        continue

      lists['abnormal'].append(user)

  return lists

def getSliceIterator(user_ids):
  for i in range(0, len(user_ids), 100):
    yield user_ids[i:i+100]
