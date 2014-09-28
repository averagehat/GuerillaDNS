worksregex = r'class="tr.".+edit_domain_id=([0-9]+)>([a-zA-Z0-9]+\.[a-z]+)<.+\(([0-9]+)\ h.+((public)|(private)).+\(([0-9]{2}\/[0-9]{2}\/[0-9]{4})\)'


rx = r'class="tr.".+edit_domain_id=([0-9]+)>([a-zA-Z0-9]+\.[a-z]+)<'
nuregex = r'class="tr.".+edit_domain_id=([0-9]+)>([a-zA-Z0-9]+\.[a-z]+)<.+\(([0-9]+)\ h'

regex = r'class="tr.".+edit_domain_id=([0-9]+).+>([a-Z0-9]+\.+)<.+\(([0-9]+)\)\ hosts.+((public)|(private)).+\(([0-9]{2}\/[0-9]{2}\/[0-9]{4})\)'




url = 'http://freedns.afraid.org/domain/registry/?sort=2&page=1'


import time
import requests
import re
from datetime import datetime
import mymongo
'''
stillpublic: because we're sorting by status (public|private) we will eventually hit a page where everything past it is
private, so we stop there.
pagenum: iterate through each page
sort: sort by status
regex: matches groups in the form (id (url), domain name, # hosts, status, datecreated)
'''


# Start real code
# matches privates: domainre =  r'class="tr.".+edit_domain_id=([0-9]+)>([a-zA-Z0-9]+\.[a-z]+)<.+\(([0-9]+)\ h.+(public|private).+\(([0-9]{2}\/[0-9]{2}\/[0-9]{4})\)'
domainre =  r'class="tr.".+edit_domain_id=([0-9]+)>([a-zA-Z0-9]+\.[a-z]+)<.+\(([0-9]+)\ h.+(public).+\(([0-9]{2}\/[0-9]{2}\/[0-9]{4})\)'

url = 'http://freedns.afraid.org/domain/registry/'

mymongo = mymongo.MyMongo()
page = 0
while stillpublic:
  time.sleep(.3)
  pagenum += 1
  
  #sort=2 sorts by status (public v. private)
  params = {'page' : pagenum, 'sort' : 2}
  r = requests.get(url, params=params)
  # example:  ('24459', 'ricardo24.ch', '56', 'public', '07/22/2004'),

  matches = re.findall(domainre, r.text)
  if not matches or len(matches) == 0:
    stillpublic = False
    print ' Ran out of public domains at page  ' + str(pagenum)
  else:
    for domain in matches:
      storedomain(domaintuple)
    print 'Stored ' + str(len(matches)) + ' public domains from page ' + str(pagenum)



def storedomain(domaintuple):
  id, domainname, hosts, status, createDate = domaintuple
  id, hosts = int(id), int(hosts)
  ispublic = (status == 'public')
  dt = datetime.strptime(d, '%m/%d/%y')
  if not mymongo.domains.find_one({'webid' : id}):
    mymongo.domains.insert({'webid' : id, 'domainName' : domainname, 'hosts' : int(hosts), 'isPublic' : ispublic, 'createTime' : dt})

