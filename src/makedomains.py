from mymongo import MyMongo
from dnsclient import DNSClient
import random
import time
import os
dns_username = os.environ['FDNS_UN']
dns_password = os.environ['FDNS_PW']
mandrill_2 = os.envrion['MANDRILL_1']
mandrill_2 = os.envrion['MANDRILL_2']
dns = DNSClient(dns_username, dns_username)
dns.login()
connection = MyMongo()
dc= connection.domains
wordsfile = open('../data/words.txt')
words = wordsfile.read()
random.seed(time.time())
cur=dc.find({'createTime' : {'$gte' : start},  'domainName': {'$not' : reg}})
chars = ['-','.']

def getword(): 
    line = words[random.uniform(0, len(words) - 1)]
    return line.replace(' ', '-')

def randomchar(): return chars[random.uniform(0, len(chars) -1)]

def getdomain():    return cursor.next()

def coinflip(): return random.uniform(1,2) %2

def getsubstring(): 
    word1, word2 = getword(), getword()
    if coinflip(): result = randomchar().join(word1, word2)
    else: result = word1
    if len(result) > 14: result = result[:15]
    return result
    
while count < 20:
    record_type = 'MX'
    
    d = getdomain()
    domain_id, domain_str = d['webid'], d['name']
    substring = getsubstring()
    for dest_str in [mandrill_1, mandrill_2]:
        dns.addsubdomain(domain_id, substring, 'MX', dest_str)

    count += 1
    dc.update({'webid' : domain_id : {'$set' : {'using' : True}} )
   




