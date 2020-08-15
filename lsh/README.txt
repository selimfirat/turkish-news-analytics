**** LSH - ApacheBeam *****

	*	corpus_lsh.py is the python file that we have tested our lsh Apache Beam
		implementation on corpusdataset.txt the result of this python file is 
		"outcorpus" run as : python corpus_lsh.py

	    to get more information about corpus dataset go to = https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html#Download
		corpus-final09.xls has the categories of the plagiarised homeworks
		cut means copy and paste(start and end points are not same),
		light means slightly revisioned version of original homework(high similarity)
		heavy means heavily revisioned version of original homework  (low similarity)
		non means it is an original homework(almost non siimilarity)

		to evaluate the lsh run checklshout.py and get evaluation output printed on terminal




	*	news_lsh.py is the python file that we have tested our lsh Apache Beam
		implementation on our own news dataset which is news.json, 
		the result of this python file is "outnews" 
		(	note: this can take up to 14 minutes as news.json is 300 MB but we get clusters of similar news as output :D )
		(	
			note2: pairwise result of the pipeline is commented out because it takes 
			3 hours and 15 gb ram to show pairwise output - you can test if you want to.
			Output of 14 minute run is the cluster of similar news so it works fine
		)
		run as : python news_lsh.py




**** Kibana For Dataset and Results Visualization ****

	* to create a cluster and get elasticsearch and kibana endpoints go to = https://www.elastic.co/cloud
		

	* once you create a cluster you will receive password , kibana_endpoint, and elsaticsearch_endpoint like ours as belows:
		username: elastic
		pasword : JFSEs3GIGmuB5W0VZNGyFJPy

		kibana: https://934b84c4c59ac5f737fcb609076603d8.us-east-1.aws.found.io:9243

		elastic: https://ffc97d66cc49d80123c71f8d348824e1.us-east-1.aws.found.io:9243
	* then run :
		*news_kibana.py to convert news.json to elastice and get news_kibana output 
		*doc_sentiment_kibana.py to convert doc_sentiment.txt to elasticsearch and get doc_sentiment output
		*nes.py to convert ne_sentiment.txt to elastic search and get LOC,ORG,PER outputs
	* then upload these outputs to elastic search as:
		* curl -u elastic -H 'Content-Type: application/x-ndjson' -XPOST 'https://ffc97d66cc49d80123c71f8d348824e1.us-east-1.aws.found.io:9243/_bulk' --data-binary @PER 

	* we are ready to visualize in kibana at endpoint = https://934b84c4c59ac5f737fcb609076603d8.us-east-1.aws.found.io:9243

