import requests
import re
import warnings
class DNSClient(object):

   def __init__(self, username, password):
      self.un, self.pw = username, password
      self.session = requests.Session()
      self.headers =  self.pl =  self.params = {}
      self.valid_dest_types = [ 'A', 'AAAA', 'CNAME', 'NS', 'MX', \
            'TXT', 'SPF', 'SPF', 'LOC', 'HINFO', 'RP', 'SRV', 'SSHFP']
      self.baseurl = 'http://freedns.afraid.org'
      self.authenticated = False

      self.default_headers = {'content-type' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

   def _makerequest(self, url, method):
      error_string=None
      if method == 'GET':
         r= self.session.get(url, headers=self.headers)
      elif method == 'POST': r= self.session.post(url, headers=self.headers, params=self.params) 
      else:
         raise Exception("_makerequest only takes 'GET' and 'POST' methods")
      if not r.status_code == 200: 
         error_string = "Bad response code:  " + str(r.status_code)
      else:  error_string = self.get_page_errors(r)
      if error_string:
         warnings.warn(method + ' @ ' + url + ' failed. These are the Errors:\n' + error_string)
      return r, error_string

   def get_page_errors(self, response):
      has_error_re=r'(?:<.+?>[^<>]*?)([0-9]\serrors?)(?:[^<>]*?<.+?>)'
     # errors_re = r'(?:<.+?>[^<>]*?)">("?[\(\)\@\,\s\"\+\?\-a-zA-Z0-9\.]+"?)|(?:\s)(?:[^<>]*?<.+?>)'
    #  errors_re = r'(?:<.+?>[^<>]*?)<li>("?[\(\)\@\,\s\"\+\?\-a-zA-Z0-9\.\n]+"?)(?:[^<>]*?<.+?>)'
     # errors_re = r'(?:<.+?>[^<>]*?)<li>((.|\n)+)</font>(?:[^<>]*?<.+?>)'
      errors_re = r'(?:<.+?>[^<>]*?)<li>("?[\(\)\@\,\s\"\+\?\-a-zA-Z0-9\.|\n]+"?)(?:[^<>]*?<.+?>)'
     # errors_re = r'(?:<.+?>[^<>]*?)\<li\>(.+)\<\/font\>(?:[^<>]*?<.+?>)'
     # errors_re = r'(?:<.+?>[^<>]*?)\<li\>(.+)\<\/font\>'

      has_error = re.findall(has_error_re, response.text)
      print has_error
      if has_error:
         has_error.extend(re.findall(errors_re, response.text))
         error_string = '\n--'.join(has_error)
         return error_string
      else: return None

   def login(self):
      url = 'http://freedns.afraid.org/zc.php?step=2'
      self.headers =  {'content-type' : 'application/x-www-form-urlencoded'}
#      self.params =  { 'username' : self.un, 'password' : self.pw, 'submit' : 'Login', 'remote' : '', 'from' : 'L3ByZW1pdW0vYml0Y29pbi8=', 'action' : 'auth'}
      self.params =  { 'username' : self.un, 'password' : self.pw, 'submit' : 'Login', 'remote' : '', 'action' : 'auth'}
      response, error_string =  self._makerequest(url, 'POST')
      return response
      

   def addsubdomain(self, domain_id, subdomain, dest_type, dest_address):
      if not dest_type in self.valid_dest_types:
         raise Exception("Not a valid destination type, must be one of: \n " + str(self.valid_dest_types) )
      # validate the other fields
      self.headers = self.default_headers
      self.params = {'type' : dest_type, 'subdomain' : subdomain, 'domain_id' : domain_id, \
            'address' : dest_address}
      self.url  = 'http://freedns.afraid.org/subdomain/save.php?step=2'
      r, error = self._makerequest(self.url, 'POST')
      return r


   def newsession(self, username, password):
      self.un, self.pw = username, password
      self.session = requests.Session()
      self.authenticated = False
      return self.login()

  #use decorators on functions that require login?

#returns user's own subdomains
   def get_subdomains(self, domain_filter=''):
      url = 'https://freedns.afraid.org/subdomain/'
      r, errors = self._makerequest(url, 'GET')
#      subdomains_re = r'(?:data_id=([0-9]+)\>([a-zA-Z\.0-9-]+.[a-zA-Z]{2,}))+'# returns subdomains w/ ids grouped by larger domain
      subdomains_re = r'(?:data_id=([0-9]+)\>([a-zA-Z\.0-9-]+.[a-zA-Z]{2,})(?:</a></td><td\s?[a-z]+........>)([A-Z]+)(?:[</a-z\s#>=]+)([0-9:a-zA-Z\.]+))'

      matches = re.findall(subdomains_re, r.text)
      subdomains = []
      for m in matches:
         _id,  name, dest_type, dest_address  = m
         if domain_filter in name:
            subdomains.append( {'name' : name, 'id' : _d, 'dest_type' : dest_type, 'dest_address' : dest_address})
      return subdomains

  

   def remove_subdomain(self, sub_id):
       url = 'http://freedns.afraid.org/subdomain/delete2.php'
       self.params = {'data_id[]' : sub_id, 'submit' : 'delete selected'}
       self.headers=self.default_headers
       self._makerequest(url, 'POST')



  
