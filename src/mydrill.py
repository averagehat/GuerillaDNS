import mandrill
from makedomains import dc as domain_collection
import os

webhook_url = os.environ['MANDRILL_APP_URL']
mandrill_key = os.environ['MANDRILL_API_KEY'] 
inbound = mandrill.Mandrill(mandrill_key).inbound

def add_webhooks():
    
    for domain in domain_collection.find({'using' : True}):
        name = domain['domainName']
        print inbound.add_domain(domain=name)
        print inbound.add_route(name, '*', webhook_url)

        domain_collection.update({'domainName' : name }, { '$set' : { 'mandrillActivated' : True} } )

if __name__ == '__main__':
    add_webhooks()
