import pymongo
import urlparse 
 


class MyMongo:
  def __init__(self):

    MONGO_URL = os.environ.get('MONGOHQ_URL')
    if MONGO_URL:
      connection = pymongo.Connection(MONGO_URL)
      database = connection[urlparse.urlparse(MONGO_URL).path[1:]]
      botdb = database.botdb
      providers = database.providers
      domains = database.domains
   
    self.botdb = botdb
    self.providers = providers
    self.domains = domains

  def close():
    self.connection.close()
