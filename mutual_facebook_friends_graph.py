__author__ = 'zekaidis'

import networkx
import requests
import json
import facebook

from networkx.readwrite import json_graph

#TODO: Implement pagination if needed!

#Get your access token right, for ex. for mining friends, you need to check specific boxes under friends_permissions tab
ACCESS_TOKEN = ''

g = facebook.GraphAPI(ACCESS_TOKEN)

friends = [(friend['id'],friend['name']) for friend in g.get_connections("me","friends")['data']]

#Using unversioned api not 1.0, 2.0 or 2.1
url = 'https://graph.facebook.com/me/mutualfriends/%s?access_token=%s'

mutual_friends = {}

for friend_id, friend_name in friends:
    r = requests.get(url % (friend_id, ACCESS_TOKEN,))
    resp = json.loads(r.content)['data']
    mutual_friends[friend_name] = [data['name'] for data in resp]

graph = networkx.Graph()

[ graph.add_edge('me', friend) for friend in mutual_friends]

[graph.add_edge(m1, m2)
 for m1 in mutual_friends
    for m2 in mutual_friends[m1] ]

graph_dump = json_graph.node_link_data(graph)

json.dump(graph_dump, open('graph_data.json','w'))

