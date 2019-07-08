from django.contrib.auth import get_user_model
from django.test import TestCase
from webdriver_manager.chrome import ChromeDriverManager
import time
# Create your tests here.
from ..accounts.models import UserProfile

User = get_user_model()
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username =  'lior'
password = '123456789a'
email    = 'l@gmail.com'


class RegTestCase(LiveServerTestCase):

    def setUp(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        self.selenium = webdriver.Chrome(ChromeDriverManager().install())
        super(RegTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(RegTestCase, self).tearDown()
    @property
    def set(self):
        #Opening the link we want to tes
        time.sleep(3)
        #find the form element
        self.selenium.get("%s%s" % (self.live_server_url, '/register/'))
        username = self.selenium.find_element_by_id('id_username')
        email = self.selenium.find_element_by_id('id_email')
        password1 = self.selenium.find_element_by_id('id_password')
        password2 = self.selenium.find_element_by_id('id_password2')
        username.send_keys(self.username)
        email.send_keys(self.email)
        password1.send_keys(self.password1)
        password2.send_keys(self.password2)
        time.sleep(3)
        self.selenium.find_element_by_id('reg').click()
        time.sleep(3)
        
    def test_register(self):
        self.selenium.get("%s%s" % (self.live_server_url, '/register/'))
        self.email,self.password1,self.password2,self.username=email,password,password,username
        self.set
        element = self.selenium.find_element_by_tag_name('h1')
        assert element.text == 'Login'
        time.sleep(3)       

    def test_dup_user(self):
        self.email,self.password1,self.password2,self.username=email,password,password,username
        self.set

        self.email,self.password1,self.password2,self.username=email+'1',password,password,username
        self.set

        #Fill the form with data
        assert self.selenium.find_element_by_id('error_1_id_username')
        time.sleep(3)

    def test_dup_mail(self):
        self.email,self.password1,self.password2,self.username=email,password,password,username
        self.set
        self.email,self.password1,self.password2,self.username=email,password,password,username+'1'
        self.set
        #Fill the form with data
        assert self.selenium.find_element_by_id('error_1_id_email')
        time.sleep(3)


    def test_pass_do_not_mutch(self):
        self.email,self.password1,self.password2,self.username=email,password,password,username
        self.set
        self.email,self.password1,self.password2,self.username=email,password,password+'1',username
        self.set
        #Fill the form with data
        assert self.selenium.find_element_by_id('error_1_id_password2')
        time.sleep(3)





class LoginTestCase(LiveServerTestCase):

    def setUp(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--headless")
        self.selenium = webdriver.Chrome(ChromeDriverManager().install())
        super(LoginTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(LoginTestCase, self).tearDown()
    @property
    def set(self):
        #Opening the link we want to tes
        time.sleep(3)
        #find the form element
        self.selenium.get("%s%s" % (self.live_server_url, '/register/'))
        username = self.selenium.find_element_by_id('id_username')
        email = self.selenium.find_element_by_id('id_email')
        password1 = self.selenium.find_element_by_id('id_password')
        password2 = self.selenium.find_element_by_id('id_password2')
        username.send_keys(self.username)
        email.send_keys(self.email)
        password1.send_keys(self.password1)
        password2.send_keys(self.password2)
        time.sleep(3)
        self.selenium.find_element_by_id('reg').click()
        time.sleep(3)
    @property
    def set_log(self):
        self.selenium.find_element_by_id('id_password').send_keys(self.password3)
        self.selenium.find_element_by_id('id_username').send_keys(self.user1)
        self.selenium.find_element_by_id('loginb').click()
        
    def test_login(self):
        self.email,self.password1,self.password2,self.username,self.user1,self.password3=email,password,password,username,username,password
        self.set
        self.set_log
        assert self.selenium.find_element_by_id('div_id_content')

    def test_user_not_exists_in_db(self):
        time.sleep(3)
        self.email,self.password1,self.password2,self.username,self.user1,self.password3=email,password,password,username,username+'1',password
        self.selenium.get("%s%s" % (self.live_server_url, '/login/'))
        self.set_log
        element = self.selenium.find_element_by_tag_name('p')
        assert element.text == "Your username and password didn't match. Please try again." 
   
    def test_pass_not_exists_in_db(self):
        time.sleep(3)
        self.email,self.password1,self.password2,self.username,self.user1,self.password3=email,password,password,username,username,password+'2'
        self.selenium.get("%s%s" % (self.live_server_url, '/login/'))
        self.set_log
        element = self.selenium.find_element_by_tag_name('p')
        assert element.text == "Your username and password didn't match. Please try again."   

    def test_blank_pass(self):
        time.sleep(3)
        self.email,self.password1,self.password2,self.username,self.user1,self.password3=email,password,password,username,username,''
        self.selenium.get("%s%s" % (self.live_server_url, '/login/'))
        self.set_log
        assert self.selenium.find_element_by_id('loginb') 


"""

 
"""
