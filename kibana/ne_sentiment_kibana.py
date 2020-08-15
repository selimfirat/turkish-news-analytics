
"""

Author : Berk Mandiracioglu


"""

import glob
import codecs
from urllib.parse import urlparse
from math import log10, floor

file = open('sentiment_ne_kibana','w') 


for filename in glob.glob('ne_sentiment.txt'):
	text = ""

	with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as f:
		for line in f:
			words = eval(line)
			file.write('{"index":{"_index":"sentandnes","_type":"article"}}\n')
			file.write('{"namedentity":"')
			#print(words[0])
			file.write(words[1])
			file.write('","score":"')
			#print(words[1],"%.2f" % round(float(words[1]),2))
			file.write("%.2f" % round(float(words[2]),2))
			file.write('"}\n')

		
  		

  	

file.close()
