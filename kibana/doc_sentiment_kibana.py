"""

Author : Berk Mandiracioglu


"""


import glob
import codecs
from urllib.parse import urlparse
from math import log10, floor

file = open('doc_sentiment','w') 


for filename in glob.glob('doc_sentiment.txt'):
	text = ""

	with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as f:
		for line in f:
			words = line.split()
			file.write('{"index":{"_index":"news","_type":"article"}}\n')
			file.write('{"domain":"')
			#print(words[0])
			file.write(urlparse(words[0]).netloc)
			file.write('","score":"')
			#print(words[1],"%.2f" % round(float(words[1]),2))
			file.write("%.2f" % round(float(words[1]),2))
			file.write('"}\n')

		
  		

  	

file.close()
