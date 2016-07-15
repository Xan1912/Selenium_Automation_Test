from selenium.webdriver.common.keys import Keys
from validate_email import validate_email
from selenium import webdriver
import dns.resolver
import socket
import smtplib
import unittest
import re

class HootTest(unittest.TestCase):
	
	def setUp(self):
		self.driver = webdriver.Firefox()
	
	def testSearch(self):
		driver = self.driver
		driver.get("https://stage.hootboard.com/b/12788/QA_Testing_Board")
		
		driver.implicitly_wait(10)
		login = driver.find_element_by_link_text("Log In")
		login.click()
		
		driver.implicitly_wait(10)
		userID = driver.find_element_by_id("emailInput")
		
		driver.implicitly_wait(10)
		userPass = driver.find_element_by_name("password")
		
		userID.send_keys("qatester@raspee.com")
		userID.send_keys(Keys.RETURN)
		
		userPass.send_keys("hootboard")
		userPass.send_keys(Keys.RETURN)
		
		driver.implicitly_wait(10)
		signIn = driver.find_element_by_xpath("//button[@class='btn btn-success btn-lg']")
		signIn.click()

		driver.implicitly_wait(30)
		invite = driver.find_element_by_xpath('//*[@id="ribbon-invite-a"]/span')
		invite.click()

		driver.implicitly_wait(30)
		posters = driver.find_element_by_xpath('//div[@class="text-wrap"]/h2')
		posters.click()

		emailIDs = raw_input("Mail(s)?:")

		driver.implicitly_wait(30)
		email = driver.find_element_by_id('emailAdds')
		email.send_keys(emailIDs)
		
		mails = emailIDs.split(',')
		
		for mail in mails:
			addressToVerify = mail
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
			if match == None:
				print "Please enter a valid mail ID"
		
			is_valid = validate_email(mail, verify = True)
			if is_valid == False:
				print "Please enter a valid mail ID"
			
		driver.implicitly_wait(40)
		send_invite = driver.find_element_by_xpath('//button[@class="btn btn-success btn-lg"]')
		send_invite.click()
		
		SERVER = "localhost"
		FROM = "qatester@raspee.com"
		TO = mails
		SUBJECT = "Invitation"
		TEXT = "Hey,Join our HootBoard please. It will only take 30 seconds but it's worth it. It's a great way for us to post announcements, policies & events publicly OR privately. We can also use it as a forum or as a way to recognize our achievements.Once you open the board click 'Accept Invitation'."
		
		message = """\
		From: %s
		To: %s
		Subject: %s
		%s
		""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
		
		server = smtplib.SMTP(SERVER)
		server.sendmail(FROM, TO, message)
		server.quit()

if __name__ == "__main__":
    unittest.main()