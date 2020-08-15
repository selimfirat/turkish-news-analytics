from google.cloud import datastore

class DataStorePipeline(object):

    def open_spider(self, spider):
        return

    def close_spider(self, spider):
        return


    def process_item(self, item, spider):
        # Create, populate and persist an entity
        # Instantiates a client
        datastore_client = datastore.Client()

        # The kind for the new entity
        kind = 'Article'
        # The name/ID for the new entity
        url = item['full_url']
        # The Cloud Datastore key for the new entity
        task_key = datastore_client.key(kind, url)


        # Prepares the new entity
        task = datastore.Entity(key=task_key, exclude_from_indexes=["date_publish", "date_download", "description", "text", "title"])
        task.update(item)

        # Saves the entity
        datastore_client.put(task)

        return item