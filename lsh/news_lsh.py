"""

Author : Berk Mandiracioglu


"""

from __future__ import absolute_import
import json as simplejson
import argparse
import logging
import re
from urlparse import urlparse
import glob
import binascii
import six
import itertools
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

from apache_beam.options.pipeline_options import  PipelineOptions, GoogleCloudOptions, StandardOptions, SetupOptions
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/cs342/Downloads/My First Project-1b53f4c43fc3.json"
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
  		yield (''.join(str(x) for x in result[lower:upper]),minsig[0])
  		
  	
  def convertToJsonObj(jsonText):
        return simplejson.loads(jsonText)

  def showCandidatePairs(buckets):
    for subset in itertools.combinations(buckets[1], 2):
  		#parsed0 = urlparse(subset[0]).netloc
  		#parsed1 = urlparse(subset[1]).netloc
  		if subset[0] > subset[1]:
  			yield ((subset[0] +' ' +subset[1]),1)
  		else:
  			yield ((subset[0] + ' '+subset[1]),1)

 

  def convertToObject(jsonObj):
  	x = jsonObj

        obj = {
            "title": x.get("properties", {}).get("title", {}).get("stringValue", ""),
            "link": x.get("properties", {}).get("link", {}).get("stringValue", ""),
            "published": x.get("properties", {}).get("published", {}).get("stringValue", ""),
            "description": x.get("properties", {}).get("np_description", {}).get("stringValue", ""),
            "content": x.get("properties", {}).get("text", {}).get("stringValue", ""),
        }

        obj["key"] = obj["link"] if obj["link"] else str(uuid.uuid4())

        return obj


  
 
  def shing(obj,k):
    result = set()
    line = obj["title"] +  obj["content"] + obj["description"]
    index = obj["key"]
    words = line.split()
    for i in range(len(words)-k+1):

  		#shingle generations k shingles
  		shingle = ""
  		for j in range(i,i+k):
  			shingle += words[j] + " "

  		hShingle = binascii.crc32(shingle.encode('utf-8')) & 0xffffffff 	
  		if hShingle not in result:

  			result.add(hShingle)

    return (index, list(result))
	
	
		

	

	



  


  pipeline_options = PipelineOptions()
  pipeline_options.view_as(SetupOptions).save_main_session = True
  pipeline_options.view_as(StandardOptions).runner = 'DirectRunner'
 
  inde = 0
  
  with beam.Pipeline(options=pipeline_options) as p:
  
	
	  
	  
		
	#pipeline to parse input news.json 	
	lines = (p | ReadFromText("news.json",coder=beam.coders.coders.StrUtf8Coder())| "Convert to Json " >> beam.Map(convertToJsonObj)| "Convert to Python Object" >> beam.Map(convertToObject))
  
  #pipeline to output <bucket, list of similar news> in lsh mapreduce implementation(takes 15 minutes)
	counts = (lines|"Read From Text" >> (beam.Map(lambda x :shing(x,5)))|"Banding and Hashing" >> beam.FlatMap(lambda x: apply(x,a,b,20,num_hash))| "Buckets Output">>beam.GroupByKey()|"filt">> beam.Filter(lambda x: len(list(x[1]))> 1) )

  #this part is to get all candidate pairs but takes 3 hours and requires 10-15 gb ram
  #counts = (counts |"show final result">>beam.FlatMap(lambda x: showCandidatePairs(x))|"en son">>beam.GroupByKey())
	
	  	

	#output
	output = counts | WriteToText("out")


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
