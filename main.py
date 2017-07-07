import requests
import json
import os

fp_cart_id = ''
jd_cart_id = ''
sz_cart_id = ''

def cls():
	os.system('cls' if os.name=='nt' else 'clear')

class MeshAPI(object):
	def __init__(self, site):
		cls()

		self.s = requests.Session()
		self.site = site.upper()

		print "MeshAPI by Luke Davis (@R8T3D) | Site: " + self.site
		print "="*60

		if self.site == 'FP':
			self.api_key = '5F9D749B65CD44479C1BA2AA21991925'
			self.user_agent = 'FootPatrol/2.0 CFNetwork/808.3 Darwin/16.3.0'
			self.cart_id = str(fp_cart_id)
			self.sitename = 'footpatrol'

		elif self.site == 'JD':
			self.api_key = '1A17CC86AC974C8D9047262E77A825A4'
			self.user_agent = 'JDSports/5.3.1.207 CFNetwork/808.3 Darwin/16.3.0'
			self.cart_id = str(jd_cart_id)
			self.sitename = 'jdsports'

		elif self.site == 'SZ':
			self.api_key = 'EA0E72B099914EB3BA6BE90A21EA43A9'
			self.user_agent = 'Size-APPLEPAY/4.0 CFNetwork/808.3 Darwin/16.3.0'
			self.cart_id = str(sz_cart_id)
			self.sitename = 'size'
		
		self.headers = {
			'Host': 'commerce.mesh.mx',
			'Content-Type': 'application/json',
			'X-API-Key': self.api_key,
			'Accept': '*/*',
			'X-Debug': '1',
			'Accept-Language': 'en-gb',
			'User-Agent': self.user_agent,
			'MESH-Commerce-Channel': 'iphone-app',
		}

		self.s.get('https://commerce.mesh.mx/stores/' + self.sitename + '/carts/' + self.cart_id, headers=self.headers)

	def get_product_info(self, pid):
		pid = str(pid)

		params = (
			('expand', 'variations,informationBlocks,customisations'),
			('channel', 'iphone-app'),
		)

		stock_json_raw = self.s.get('https://commerce.mesh.mx/stores/' + self.sitename + '/products/' + pid, headers=self.headers, params=params).text.strip()
		stock_json = json.loads(stock_json_raw)

		try:
			product_name = str(stock_json['name'])
			print product_name
			for size in stock_json['options']:
				print size + ": " + stock_json['options'][size]['SKU']
		except:
			print "Error finding product"

		choice = raw_input("Product appears to be in stock. \nAttempt to add product to cart? (Y/N) ")
		if choice.upper() == "Y":
			self.add_to_cart(pidsize)

	def add_to_cart(self, pidsize):
		pidsize = str(pidsize)

		if self.site == 'JD':
			data = '{"contents":[{"$schema":"https:\\/\\/commerce.mesh.mx\\/stores\\/jdsports\\/schema\\/CartProduct","SKU":"' + pidsize + '","quantity":1}]}'

			ATC = self.s.put('https://commerce.mesh.mx/stores/jdsports/carts/' + self.cart_id, headers=self.headers, data=data)
		else:
			ATC = self.s.put('https://commerce.mesh.mx/stores/' + self.sitename + '/carts/' + self.cart_id + '/' + pidsize, headers=self.headers, data='{"quantity":1}')

		print "Status Code: " +  str(ATC.status_code)
		print "ATC success."

if __name__ == '__main__':
	cls()
	print "MeshAPI by Luke Davis (@R8T3D)"
	print "="*60

	site = raw_input('Site? (FP, JD, SZ) ')
	mesh = MeshAPI(site)

	choice = raw_input("What would you like to do? (ATC or INFO) ")
	if choice.upper() == "ATC":
		pidsize = raw_input("PID.SIZE? ")
		mesh.add_to_cart(pidsize)
	else:
		pid = raw_input("PID? ")
		mesh.get_product_info(pid)
