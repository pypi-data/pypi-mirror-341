import unittest
from fallexplorer.main import whois_lookup

class TestFallexplorer(unittest.TestCase):
    def test_whois_lookup(self):
        result = whois_lookup('fallexplorer.openstudy.me')
        self.assertIn('Domain Name', result)

if __name__ == '__main__':
    unittest.main()
