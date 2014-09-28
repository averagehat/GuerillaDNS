from mymongo import MyMongo
from dnsclient import DNSClient
import random, time
import os, sys
import datetime
import re
dns_username = os.environ['FDNS_UN']
dns_password = os.environ['FDNS_PW']
print dns_username
print dns_password

mandrill_1 = os.environ['MANDRILL_1']
mandrill_2 = os.environ['MANDRILL_2']
dns = DNSClient(dns_username, dns_password)
connection = MyMongo()
dc= connection.domains
wordsfile = open('../data/words.txt')
random.seed(time.time())
chars = ['-','.']


def get_recent_domains():
    reg = re.compile(r'[0-9]') # they tend to have too many numbers and look weird
    start = datetime.datetime(2014, 8, 1, 1, 1, 1, 1)
    return dc.find({'createTime' : {'$gte' : start},  'domainName': {'$not' : reg}})

def getword(): 
    line = words[random.randint(0, len(words) - 1)]
    return line

def randomchar(): return chars[random.randint(0, len(chars) -1)]

def getwords(lines):
    words = []
    for line in lines:  
        char = randomchar()
        line = line.replace(' ', char)
        line = line.replace('/', '')
        line = line.replace('"', '') 
        line = line.replace("'", '') 
        line = line.strip()
        words.append(line)
    return words

                     # if len(line) > 7: l.append(line)


def getdomain():    return cursor.next()

def coinflip(): return random.randint(1,2) %2

def getsubstring(): 
    word1, word2 = getword(), getword()
    if coinflip(): result = randomchar().join([word1, word2])
    else: result = word1
    if len(result) > 14: result = result[:15]
    return result


def adddomains(total):
    count = 0    
    while count < total:
        record_type = 'MX'
        
        d = getdomain()
        domain_id, domain_str = d['webid'], d['domainName']
        substring = getsubstring()
        subdomain = '.'.join([substring, domain_str])
        success = True
        print 'attempting ', subdomain, ' . . . . '
        for dest_str in [mandrill_1, mandrill_2]:
            response, error = dns.addsubdomain(domain_id, substring, 'MX', dest_str)
            if error: 
                success = False
                break
        if success: print subdomain, '  added'
        count += 1
        dc.update({'webid' : domain_id} , {'$set' : {'using' : success, 'subdomain' : subdomain}} )
       
    
    
    
    
if __name__ == '__main__':

    r, error = dns.login()
    if error: sys.exit(1)
    cursor = get_recent_domains()
    words = getwords(wordsfile.readlines())

    adddomains(20)
