#Guerilla DNS
*A "guerilla" API for freedns.afraid.org* 
<br> Still under development.
<br>This is for programmatically adding, changing and removing public subdomains at freedns.afraid.org.
<br> This is not a script for dynamic IP updating, although it could easily adapted for that.
<br> This is not a script for spidering freedns. 
<br> This script is intended for the management of a large number of subdomains. It uses the python requests library to login and update domains, and regular expressions to read the responses from freedns webpages. Because this script relies on web forms, it is subject to break at anytime. That's just the way it is.
<br> If you use this script, PLEASE be polite. Do not hammer freedns with this scripts. Use time.sleep(), etc.
