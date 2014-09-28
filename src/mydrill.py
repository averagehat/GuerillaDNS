import mandrill
from makedomains import dc as domain_collection
import os

webhook_url = os.environ['MANDRILL_APP_URL']
mandrill_key = os.environ['MANDRILL_API_KEY'] 
inbound = mandrill.Mandrill(mandrill_key).inbound

def add_webhooks():
    for domain in domain_collection.find({'using' : True, 'mandrillActivated' : {'$exists' : True }}):
        papa_domain, subdomain = domain['domainName'], domain['subdomain']
        try:
            inbound.delete_domain(domain=papa_domain)
        except: print ''
        print inbound.add_domain(domain=subdomain)
        print inbound.add_route(subdomain, '*', webhook_url)

#        domain_collection.update({'domainName' : name }, { '$set' : { 'mandrillActivated' : True} } )

def send_all():

    for domain in domain_collection.find({'using' : True, 'mandrillActivated' : True }):
        target = '@'.join(['test_raw_send', domain['subdomain']])
        sender= 'form_raw_send@adamevespecial.umb88.com'
        print 'Sending from ' , sender, 'to . . . ' , target
        message = 'From: ' + sender + '\nTo: ' + target + '\nSubject: Some Subject\n\nSome content.'
        print inbound.send_raw(raw_message=message, to=[target], mail_from=sender)

if __name__ == '__main__':
    send_all()
