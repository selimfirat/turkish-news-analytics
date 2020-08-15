"""

Author : Berk Mandiracioglu


"""

import json
from urllib.parse import urlparse
import pandas as pd


file = open('news_kibana','w') 
 



with open('news.json') as f:
	data = json.load(f)

for keys in data['val']:
	k = keys['key']

	pat = k['path']
	link = pat[0]['name']
	link = urlparse(link).netloc
	properties = keys['properties']
	date = properties['published']['stringValue']
	
	title = properties['title']['stringValue']
	title = title.replace("'", "")
	title = title.replace('"', '')
	title = title.replace(":" ,"")
	title = title.replace("\n" ,"")
	title = title.replace("," ,"")
	words = title.split()

	file.write('{"index":{"_index":"newswdates","_type":"article"}}\n')
	file.write('{"domain":"')
	file.write(link)
	file.write('","pdate":"')
	file.write(date)
	file.write('","title":"')
	
	file.write(title)
	file.write('","tags":')

	tagString = '['
	for w in words:
		tagString += '"'+w+ '",'

	tagString = tagString[:len(tagString)-1] + ']'
			

	file.write(tagString)
		
	file.write('}\n')

	
	
	
file.close() 

