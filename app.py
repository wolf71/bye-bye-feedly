'''
  Change Log by wolf:
   @2020/3/12  
    - using a while loop to save all of your saved articles.
    - add proxy support.
   
  # Feedly API document:
  - https://developer.feedly.com/v3/streams/
  
  # python -m http.server 
  
'''

import io
import json
import requests

# Add your feedly API credentials
# Get token : https://feedly.com/v3/auth/dev
# continuation: Optional string a continuation id is used to page through the entry ids; you can also pass a timestamp in ms, which will act as an "older than" limit.

user_id = 'your feedly api id'
access_token = 'your feedly api token'

per_page = 1000   # for tag/ max is 500 other max is 1000
# if don't using proxy, please set proxy = {}
proxy ={"http":"http://192.168.3.2:3128","https":"http://192.168.3.2:3128"}

def get_saved_items(user_id, access_token):
  headers = {'Authorization' : 'OAuth ' + access_token}
  continue_str = ''

  items = []
  run_flag, cnt = 1, 1

  while run_flag:
    url = 'https://cloud.feedly.com/v3/streams/contents?streamId=user/' + user_id + '/tag/global.saved&count='+str(per_page)+'&continuation='+continue_str

    print(cnt,' Requesting item, c_str='+continue_str)
    r = requests.get(url, headers = headers,proxies=proxy)

    if r.status_code == 200:
      filename = 'data.json'
      r.encoding = 'UTF-8'
      info = r.json()
      try:
        continue_str = info['continuation']
      except:
        # Can't get continuation,maybe last page
        run_flag = 0
      # join infos 
      items += info['items']
      cnt += 1
    else:
      print('!!!Fetch Error, Status code: ' + str(r.status_code))
      break

  # Write compact JSON
  # Replace 'separators' argument with 'indent=4' if you don’t want it minified
  info['items'] = items 
  with io.open(filename, 'w', encoding='UTF-8') as output_file:
    try:
      json.dump(info, output_file, separators=(',',':'))
      print('Save to: ' + filename)
    except ValueError as error:
      print(error)

get_saved_items(user_id, access_token)