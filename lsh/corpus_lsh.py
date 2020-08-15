"""

Author : Berk Mandiracioglu


"""

from __future__ import absolute_import

import argparse
import logging
import re
import glob
import binascii
import six
import itertools
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions, StandardOptions

import random
import codecs





def run(argv=None):
  
  num_docs = 100
  num_hash = 100
  prime = 4294967311

  N = 2**32
  #generating random hash function parameters
  a = []
  b = []
  for it in range(num_hash):
	a.append(random.randint(1,int(N/2)))
	b.append(random.randint(1,int(N/2)))

  def apply(minsig,a,b,bands,num_hash):
  	rows = num_hash / bands

  	result = []
  	for i in range(num_hash):
  		
  		res = 2**33
  		for hShingle in minsig[1]:
			res = min(res,(a[i]*hShingle+b[i])%prime)

  		
  		result.append(res)
  			
  	for j in range(bands):

		lower = int(j*rows)
		upper = int(j*rows+rows)
		yield (result[lower:upper],minsig[0])
  		
  	
  
  def showCandidatePairs(buckets):
  	if len(buckets[1]) > 1:
	  	for subset in itertools.combinations(buckets[1], 2):
	  		if subset[0]>subset[1]:
	  			yield (list((subset[1],subset[0])),1)
	  		else:
	  			yield (list(subset),1)




  

  def shing(tup,k):
  	result = set()
  	
	line, index = tup.split(',')
  	words = line.split()
  	for i in range(len(words)-k+1):

		#shingle generations k shingles
		shingle = ""
		for j in range(i,i+k):
			shingle += words[j] + " "

		hShingle = binascii.crc32(shingle.encode('utf-8')) & 0xffffffff 	
		if hShingle not in result:

			result.add(hShingle)


			yield (index, hShingle)
	
	
		

	

	



  



	
  

  
  pipeline_options = PipelineOptions()
  pipeline_options.view_as(SetupOptions).save_main_session = True
  pipeline_options.view_as(StandardOptions).runner = 'DirectRunner'
  inde = 0
  for filename in glob.glob('corpusdataset.txt'):
  	with beam.Pipeline(options=pipeline_options) as p:
  
	
	  
	  
			  
		
		
	  	
	  lines = p | ReadFromText(filename)
	  lsh = (lines|"Read From Text" >> (beam.FlatMap(lambda x :shing(x,2)))|"gruping">>beam.GroupByKey()|"banding and hashing" >> beam.FlatMap(lambda x: apply(x,a,b,25,num_hash))| "same buckets">>beam.GroupByKey()|"shoe final result">>beam.FlatMap(lambda x: showCandidatePairs(x))|"en son">>beam.GroupByKey())
	  
	 
	 
	  	

	

	  lsh | WriteToText("outcorpus")





if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
