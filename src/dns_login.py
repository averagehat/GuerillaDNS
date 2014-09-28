# -*- coding: utf-8 -*-
from selenium import selenium
import unittest, time, re

class dns_login(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://freedns.afraid.org/")
        self.selenium.start()
    
    def test_dns_login(self):
        sel = self.selenium
        sel.open("/signup/")
        sel.type("id=firstname", "fn")
        sel.type("id=lastname", "ln")
        sel.type("id=username", "username")
        sel.type("id=password", "pw")
        sel.type("id=password2", "pw")
        sel.type("id=email", "email")
        sel.type("id=captcha_code", "captch")
        sel.click("id=tos")
        sel.click("name=send")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
