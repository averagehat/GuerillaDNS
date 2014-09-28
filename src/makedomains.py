from mymongo import MyMongo
from dnsclient import DNSClient

dns_username = os.environ['FDNS_UN']
dns_password = os.envrion['FDNS_PW']

cli = DNSClient(dns_username, dns_username)
connection = MyMongo()
dc= connection.domains


