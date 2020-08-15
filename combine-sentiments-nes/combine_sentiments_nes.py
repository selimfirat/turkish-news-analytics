import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, SetupOptions
from apache_beam.io.textio import ReadFromText, WriteToText
import logging

def run():
    
    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DirectRunner'

    p = beam.Pipeline(options=options)
    

    sentiments = (p
             | "Read From Text" >> ReadFromText("doc_sentiment.txt", coder=beam.coders.coders.StrUtf8Coder()) # line by line
             | "Convert to Doc, SentimentScore Tuple" >> beam.Map(lambda x: (x.split(" ")[0], x.split(" ")[1]))
    )
    
    nes = (p
             | "Read Named Entites" >> ReadFromText("doc_nes.txt", coder=beam.coders.coders.StrUtf8Coder()) # line by line
             | "Convert to Doc, Entities Tuple" >> beam.Map(lambda x: eval(x))
    )

    def process_nes_sentiment((doc, nes_sentiment)):
        neslist = nes_sentiment["nes"]
        st = nes_sentiment["sentiment"][0]
        for nes in neslist:
            for ne in nes:
                yield (ne[0], ne[1], st)

    g = ({ "nes": nes, "sentiment": sentiments }
             | beam.CoGroupByKey()
             | beam.FlatMap(process_nes_sentiment)
    )

    (g
         | "Write Results" >> WriteToText("ne_sentiment.txt")
    )

    p.run()



logging.getLogger().setLevel(logging.INFO)
run()