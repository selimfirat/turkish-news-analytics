"""

Author : Berk Mandiracioglu


"""


import glob
import codecs
from urllib.parse import urlparse
from math import log10, floor
from ast import literal_eval as make_tuple

fileP = open('PER','w') 
fileL = open('LOC','w')
fileO = open('ORG','w') 

for filename in glob.glob('doc_nes.txt'):


	with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as f:
		for line in f:
	
			tup = make_tuple(line)
			

			perSet = set()
			locSet = set()
			orgSet = set()
			for l in tup[1]:
				
				if l[0] == 'PER':
					perSet.add(l[1])
				elif l[0] == 'ORG':
					orgSet.add(l[1])
				elif l[0] == 'LOC':
					locSet.add(l[1])

			perString = '['
			for m in perSet:
				m = str(m).replace(']','')
				m = m.replace('[','')
				m = m.replace(']','')
				m = m.replace('}','')
				m = m.replace('{','')
				m = m.replace('"','')
				m = m.replace(',','')
				#print(m)
				perString += '"'+str(m)+ '",'

			
			
			orgString = '['
			for m in orgSet:
				#print(str(m))
				m = str(m).replace(']','')
				m = m.replace('[','')
				m = m.replace(']','')
				m = m.replace('}','')
				m = m.replace('{','')
				m = m.replace('"','')
				m = m.replace(',','')
				#print(m)
				orgString += '"'+m+ '",'
			
			
			
			locString = '['
			for m in locSet:
				m = str(m).replace(']','')
				m = m.replace('[','')
				m = m.replace(']','')
				m = m.replace('}','')
				m = m.replace('{','')
				m = m.replace('"','')
				m = m.replace(',','')
				#print(m)
				locString += '"'+str(m)+ '",'

			
				

			

			if len(perString) > 1:
				perString = perString[:len(perString)-1] 
				perString += ']'
				fileP.write('{"index":{"_index":"mews3","_type":"article"}}\n')
				fileP.write('{"domain":"')
			
				fileP.write(urlparse(tup[0]).netloc)
				fileP.write('","PER":')
				fileP.write(perString)
				fileP.write('}\n')

			if len(orgString) > 1:
				orgString = orgString[:len(orgString)-1] 
				orgString += ']'
				fileO.write('{"index":{"_index":"mews3","_type":"article"}}\n')
				file.write('{"domain":"')
			
				fileO.write(urlparse(tup[0]).netloc)
				fileO.write('","PER":')
				fileO.write(orgString)
				fileO.write('}\n')

			if len(locString) > 1:
				locString = locString[:len(locString)-1] 
				locString += ']'
				fileL.write('{"index":{"_index":"mews3","_type":"article"}}\n')
				fileL.write('{"domain":"')
			
				fileL.write(urlparse(tup[0]).netloc)
				fileL.write('","PER":')
				fileL.write(locString)
				fileL.write('}\n')				
			
				



fileP.close()
fileO.close()
fileL.close()
