'''
wiki is being more serious about limiting requests - this is a new file to test the wiki api
in addition to the requests API to try and limit the total amount of requests sent
    might be able to grab all tournaments via titles within headers -- will need to look into more
'''

import requests
import json

s = requests.Session()

url = 'https://en.wikipedia.org/w/api.php'

parameters = {
    'action' : 'query',
    'meta' : 'userinfo|filerepoinfo|siteinfo',
    #'uiprop' : 'rights|ratelimits|options|blockinfo',
    'uiprop' : 'rights',
    'format' : 'json',
    'friprop' : 'name|displayname|url|rootUrl|scriptDirUrl|fetchDescription|favicon|local',
    #'siprop' : 'general|statistics|variables',
    'siprop' : 'statistics',
}

r = s.get(url=url, params=parameters)

data = r.json()

print(json.dumps(data, sort_keys=True, indent=4))
