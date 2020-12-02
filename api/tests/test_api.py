import unittest
import json
from ..api.app import app

class MyAppCase(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_bad_request(self):
		response = self.app.get("http://127.0.0.1:5000/operator/?adres")
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['error'], "400 Bad Request: Bad request")

	def test_no_address_specified(self):
		response = self.app.get("http://127.0.0.1:5000/operator/?adress=")
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['message'], "No address has been entered...")

	def test_bad_adress(self):
		response = self.app.get("http://127.0.0.1:5000/operator/?adress=123")
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['message'], "No result for the address provided. Please enter a valid address !")


	def test_adress_without_postal_code(self):
		response = self.app.get("http://127.0.0.1:5000/operator/?adress=125 rue des suisses")
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(data['message'], "Several cities have been found. Please specify your address !")

	def test_valid_adress(self):
		response = self.app.get("http://127.0.0.1:5000/operator/?adress=20 Avenue du Dr René Laennec 68100 Mulhouse")
		data = json.loads(response.get_data(as_text=True))

		self.assertEqual(data['Bouygue']['2G'], "True")
		self.assertEqual(data['Bouygue']['3G'], "True")
		self.assertEqual(data['Bouygue']['4G'], "True")

		self.assertEqual(data['Free']['2G'], "False")
		self.assertEqual(data['Free']['3G'], "True")
		self.assertEqual(data['Free']['4G'], "True")

		self.assertEqual(data['Orange']['2G'], "False")
		self.assertEqual(data['Orange']['3G'], "True")
		self.assertEqual(data['Orange']['4G'], "True")

		self.assertEqual(data['SFR']['2G'], "True")
		self.assertEqual(data['SFR']['3G'], "True")
		self.assertEqual(data['SFR']['4G'], "True")
